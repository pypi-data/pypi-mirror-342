import numpy as np
from ..optimizer.learnable_optimizer import Learnable_Optimizer


class RLEPSO_Optimizer(Learnable_Optimizer):
    def __init__(self, config):
        super().__init__(config)

        config.w_decay = True

        config.NP = 100
        self.__config = config

        self.__dim = config.dim
        self.__w_decay = config.w_decay
        if self.__w_decay:
            self.__w = 0.9
        else:
            self.__w = 0.729

        self.__NP = config.NP

        indexs = np.array(list(range(self.__NP)))
        self.__pci = 0.05 + 0.45 * np.exp(10 * indexs / (self.__NP - 1)) / (np.exp(10) - 1)

        self.__n_group = 5

        self.__no_improve = 0
        self.__per_no_improve = np.zeros((self.__NP,))
        self.fes = None
        self.cost = None
        self.log_index = None
        self.log_interval = config.log_interval
        self.__max_fes = config.maxFEs
        self.__is_done = False

    def __str__(self):
        return "RLEPSO_Optimizer"

    def init_population(self, problem):
        rand_pos = self.rng.uniform(low = problem.lb, high = problem.ub, size = (self.__NP, self.__dim))
        self.__max_velocity = 0.1 * (problem.ub - problem.lb)
        rand_vel = self.rng.uniform(low = -self.__max_velocity, high = self.__max_velocity, size = (self.__NP, self.__dim))
        self.fes = 0

        c_cost = self.__get_costs(problem, rand_pos)  # ps

        gbest_val = np.min(c_cost)
        gbest_index = np.argmin(c_cost)
        gbest_position = rand_pos[gbest_index]
        self.__max_cost = np.max(c_cost)

        self.__particles = {'current_position': rand_pos.copy(),  # ps, dim
                            'c_cost': c_cost.copy(),  # ps
                            'pbest_position': rand_pos.copy(),  # ps, dim
                            'pbest': c_cost.copy(),  # ps
                            'gbest_position': gbest_position.copy(),  # dim
                            'gbest_val': gbest_val,  # 1
                            'velocity': rand_vel.copy(),  # ps,dim
                            'gbest_index': gbest_index  # 1
                            }
        self.__no_improve -= self.__no_improve
        self.log_index = 1
        self.cost = [self.__particles['gbest_val']]
        self.__per_no_improve -= self.__per_no_improve

        if self.__config.full_meta_data:
            self.meta_X = [self.__particles['current_position'].copy()]
            self.meta_Cost = [self.__particles['c_cost'].copy()]

        return self.__get_state()

    # calculate costs of solutions
    def __get_costs(self, problem, position):
        self.fes += self.__NP
        if problem.optimum is None:
            cost = problem.eval(position)
        else:
            cost = problem.eval(position) - problem.optimum
        return cost

    def __get_v_clpso(self):
        rand = self.rng.rand(self.__NP, self.__dim)
        filter = rand > self.__pci[:, None]
        # tournament selection 2

        target_pos = self.__tournament_selection()
        pbest_clpso = np.where(filter, self.__particles['pbest_position'], target_pos)
        v_clpso = rand * (pbest_clpso - self.__particles['current_position'])
        return v_clpso

    def __tournament_selection(self):
        nsel = 2
        rand_index = self.rng.randint(low = 0, high = self.__NP, size = (self.__NP, self.__dim, nsel))

        candidate = self.__particles['pbest_position'][rand_index, np.arange(self.__dim)[None, :, None]]  # ps, dim, nsel
        candidate_cost = self.__particles['pbest'][rand_index]  # ps, dim, nsel
        target_pos_index = np.argmin(candidate_cost, axis = -1)  # shape?
        ps_index = np.arange(self.__NP)[:, None]
        target_pos = candidate[ps_index, np.arange(self.__dim)[None, :], target_pos_index]
        return target_pos

    def __get_v_fdr(self):
        pos = self.__particles['pbest_position']
        distance_per_dim = np.abs(pos[None, :, :].repeat(self.__NP, axis = 0) - pos[:, None, :].repeat(self.__NP, axis = 1))
        fitness = self.__particles['pbest']
        fitness_delta = fitness[None, :].repeat(self.__NP, axis = 0) - fitness[:, None].repeat(self.__NP, axis = 1)
        fdr = (fitness_delta[:, :, None]) / (distance_per_dim + 1e-5)
        target_index = np.argmin(fdr, axis = 1)

        dim_index = np.arange(self.__dim)[None, :]
        target_pos = pos[target_index, dim_index]

        v_fdr = self.rng.rand(self.__NP, self.__dim) * (target_pos - pos)
        return v_fdr

    # return coes
    def __get_coe(self, actions):
        assert actions.shape[-1] == self.__n_group * 7, 'actions size is not right!'
        ws = np.zeros(self.__NP)
        c_mutations = np.zeros_like(ws)
        c1s, c2s, c3s, c4s = np.zeros_like(ws), np.zeros_like(ws), np.zeros_like(ws), np.zeros_like(ws)
        per_group_num = self.__NP // self.__n_group
        for i in range(self.__n_group):
            a = actions[i * self.__n_group:i * self.__n_group + 7]
            c_mutations[i * per_group_num:(i + 1) * per_group_num] = a[0] * 0.01 * self.__per_no_improve[i * per_group_num:(i + 1) * per_group_num]
            ws[i * per_group_num:(i + 1) * per_group_num] = a[1] * 0.8 + 0.1
            scale = 1. / (a[3] + a[4] + a[5] + a[6] + 1e-5) * a[2] * 8
            c1s[i * per_group_num:(i + 1) * per_group_num] = scale * a[3]
            c2s[i * per_group_num:(i + 1) * per_group_num] = scale * a[4]
            c3s[i * per_group_num:(i + 1) * per_group_num] = scale * a[5]
            c4s[i * per_group_num:(i + 1) * per_group_num] = scale * a[6]
        return {'w': ws[:, None],
                'c_mutation': c_mutations,
                'c1': c1s[:, None],
                'c2': c2s[:, None],
                'c3': c3s[:, None],
                'c4': c4s[:, None]}

    def __reinit(self, filter, problem):
        if not np.any(filter):
            return
        rand_pos = self.rng.uniform(low = problem.lb, high = problem.ub, size = (self.__NP, self.__dim))
        rand_vel = self.rng.uniform(low = -self.__max_velocity, high = self.__max_velocity, size = (self.__NP, self.__dim))
        new_position = np.where(filter, rand_pos, self.__particles['current_position'])
        new_velocity = np.where(filter, rand_vel, self.__particles['velocity'])
        pre_fes = self.fes
        new_cost = self.__get_costs(problem, new_position)
        self.fes = pre_fes + np.sum(filter)

        filters = new_cost < self.__particles['pbest']
        new_cbest_val = np.min(new_cost)
        new_cbest_index = np.argmin(new_cost)

        filters_best_val = new_cbest_val < self.__particles['gbest_val']
        # update particles
        new_particles = {'current_position': new_position,  # bs, ps, dim
                         'c_cost': new_cost,  # bs, ps
                         'pbest_position': np.where(np.expand_dims(filters, axis = -1),
                                                    new_position,
                                                    self.__particles['pbest_position']),
                         'pbest': np.where(filters,
                                           new_cost,
                                           self.__particles['pbest']),
                         'velocity': new_velocity,
                         'gbest_val': np.where(filters_best_val,
                                               new_cbest_val,
                                               self.__particles['gbest_val']),
                         'gbest_position': np.where(np.expand_dims(filters_best_val, axis = -1),
                                                    new_position[new_cbest_index],
                                                    self.__particles['gbest_position']),
                         'gbest_index': np.where(filters_best_val, new_cbest_index, self.__particles['gbest_index'])
                         }
        self.__particles = new_particles

    def __get_state(self):
        return np.array([self.fes / self.__max_fes])

    def update(self, action, problem):
        is_end = False

        pre_gbest = self.__particles['gbest_val']
        # input action_dim should be : bs, ps
        # action in (0,1) the ratio to learn from pbest & gbest
        rand1 = self.rng.rand(self.__NP, 1)
        rand2 = self.rng.rand(self.__NP, 1)

        # update velocity
        v_clpso = self.__get_v_clpso()
        v_fdr = self.__get_v_fdr()
        v_pbest = rand1 * (self.__particles['pbest_position'] - self.__particles['current_position'])
        v_gbest = rand2 * (self.__particles['gbest_position'][None, :] - self.__particles['current_position'])
        coes = self.__get_coe(action)

        new_velocity = coes['w'] * self.__particles['velocity'] + coes['c1'] * v_clpso + coes['c2'] * v_fdr + coes['c3'] * v_gbest + coes['c4'] * v_pbest

        new_velocity = np.clip(new_velocity, -self.__max_velocity, self.__max_velocity)

        # update position
        new_position = self.__particles['current_position'] + new_velocity
        new_position = np.clip(new_position, problem.lb, problem.ub)

        # get new_cost
        new_cost = self.__get_costs(problem, new_position)

        filters = new_cost < self.__particles['pbest']
        new_cbest_val = np.min(new_cost)
        new_cbest_index = np.argmin(new_cost)

        filters_best_val = new_cbest_val < self.__particles['gbest_val']
        # update particles
        new_particles = {'current_position': new_position,  # bs, ps, dim
                         'c_cost': new_cost,  # bs, ps
                         'pbest_position': np.where(np.expand_dims(filters, axis = -1),
                                                    new_position,
                                                    self.__particles['pbest_position']),
                         'pbest': np.where(filters,
                                           new_cost,
                                           self.__particles['pbest']),
                         'velocity': new_velocity,
                         'gbest_val': np.where(filters_best_val,
                                               new_cbest_val,
                                               self.__particles['gbest_val']),
                         'gbest_position': np.where(np.expand_dims(filters_best_val, axis = -1),
                                                    new_position[new_cbest_index],
                                                    self.__particles['gbest_position']),
                         'gbest_index': np.where(filters_best_val, new_cbest_index, self.__particles['gbest_index'])
                         }

        # see if any batch need to be reinitialized
        if new_particles['gbest_val'] < self.__particles['gbest_val']:
            self.__no_improve = 0
        else:
            self.__no_improve += 1

        filter_per_patience = new_particles['c_cost'] < self.__particles['c_cost']
        self.__per_no_improve += 1
        tmp = np.where(filter_per_patience, self.__per_no_improve, np.zeros_like(self.__per_no_improve))
        self.__per_no_improve -= tmp

        self.__particles = new_particles
        # reinitialize according to c_mutation and per_no_improve
        filter_reinit = self.rng.rand(self.__NP) < coes['c_mutation'] * 0.01 * self.__per_no_improve
        self.__reinit(filter_reinit[:, None], problem)

        if self.fes >= self.log_index * self.log_interval:
            self.log_index += 1
            self.cost.append(self.__particles['gbest_val'])

        if self.__config.full_meta_data:
            self.meta_X.append(self.__particles['current_position'].copy())
            self.meta_Cost.append(self.__particles['c_cost'].copy())

        if problem.optimum is None:
            is_end = self.fes >= self.__max_fes
        else:
            is_end = self.fes >= self.__max_fes 

        # cal the reward
        if self.__particles['gbest_val'] < pre_gbest:
            reward = 1
        else:
            reward = -1
        next_state = self.__get_state()

        if is_end:
            if len(self.cost) >= self.__config.n_logpoint + 1:
                self.cost[-1] = self.__particles['gbest_val']
            else:
                while len(self.cost) < self.__config.n_logpoint + 1:
                    self.cost.append(self.__particles['gbest_val'])

        info = {}
        return next_state, reward, is_end, info
