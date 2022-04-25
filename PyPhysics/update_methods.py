def euler_update(r_n, v_n, a_n, time_step):
    r_n_1 = r_n + time_step * v_n
    v_n_1 = v_n + time_step * a_n

    return r_n_1, v_n_1


def euler_cromer_update(r_n, v_n, a_n, time_step):
    v_n_1 = v_n + time_step * a_n
    r_n_1 = r_n + time_step * v_n_1

    return r_n_1, v_n_1


def midpoint_update(r_n, v_n, a_n, time_step):
    v_n_1 = v_n + time_step * a_n
    r_n_1 = r_n + time_step * v_n + 0.5 * (time_step ** 2) * a_n

    return r_n_1, v_n_1
