import sys
from collect_kbo_player_data import *
sys.path.insert(0, '/Users/joshuakim/PycharmProjects/Math_Tools')
from matrix import *


pd.set_option('display.max_columns', 30)


def generate_transition_matrix(hitter_id, pitcher_id=None, consider='0010'):

    """
    :param hitter_id: between 10000 and 99999 (5-digit positive integer)
    :param consider: |hitter_total|pitcher_total|hitter_current|pitcher_current|
    :return: a list containing five 25x25 probability matrix
    """

    HITTER_WEIGHT = 2
    PITCHER_WEIGHT = 1

    # block matrices initialized
    A0, B0, C0, A1, B1, A2 = [Matrix(8, 8) for _ in range(6)]
    D0, E1, F2 = [Matrix(8, 1) for _ in range(3)]
    zero_matrix = Matrix(8, 8)
    zero_row = Matrix(1, 24)
    zero_column = Matrix(8, 1)
    one_matrix = Matrix(1, 1, [1])

    considered_data = []
    PA = 0.0
    HR = 0.0
    OneBase = 0.0
    OneHit = 0.0
    TwoHit = 0.0
    ThreeHit = 0.0
    BBHBP = 0.0
    GDP = 0.0
    GTP = 0.0
    GSP = 0.0

    if consider == '1000':
        considered_data = get_total_data(hitter_id, "Hitter")
        PA = float(considered_data['AB'] + considered_data['BB'] + considered_data['HBP'] + considered_data['GDP'])
        HR = float(considered_data['HR']) / PA
        OneBase = float(considered_data['H'] - considered_data['2B'] - considered_data['3B'] - considered_data['HR'] +
                        considered_data['BB'] + considered_data['HBP']) / PA
        OneHit = float(
            considered_data['H'] - considered_data['2B'] - considered_data['3B'] - considered_data['HR']) / PA
        TwoHit = float(considered_data['2B']) / PA
        ThreeHit = float(considered_data['3B']) / PA
        BBHBP = float(considered_data['BB'] + considered_data['HBP']) / PA
        GDP = float(considered_data['GDP']) / PA
        GTP = 692.0 / 14000000.0  # historically defined times of triple plays
        GSP = (float(considered_data['AB'] + considered_data['BB'] + considered_data['HBP'] - considered_data[
            'H'] - GDP) / PA) - GTP  # times of single plays
        # 1B = H - 2B - 3B - HR
    elif consider == '0010':
        considered_data = get_current_data(hitter_id, "Hitter")
        PA = float(considered_data['AB'] + considered_data['BB'] + considered_data['HBP'] + considered_data['GDP'])
        HR = float(considered_data['HR']) / PA
        OneBase = float(considered_data['H'] - considered_data['2B'] - considered_data['3B'] - considered_data['HR'] +
                        considered_data['BB'] + considered_data['HBP']) / PA
        OneHit = float(
            considered_data['H'] - considered_data['2B'] - considered_data['3B'] - considered_data['HR']) / PA
        TwoHit = float(considered_data['2B']) / PA
        ThreeHit = float(considered_data['3B']) / PA
        BBHBP = float(considered_data['BB'] + considered_data['HBP']) / PA
        GDP = float(considered_data['GDP']) / PA
        GTP = 692.0 / 14000000.0  # historically defined times of triple plays
        GSP = (float(considered_data['AB'] + considered_data['BB'] + considered_data['HBP'] - considered_data[
            'H'] - GDP) / PA) - GTP  # times of single plays
        # 1B = H - 2B - 3B - HR
    elif consider == '0011':
        if pitcher_id == None:
            raise Exception("No pitcher ID")
        hitter_data = get_current_data(hitter_id, "Hitter")
        pitcher_data = get_current_data(pitcher_id, "Pitcher")
        PA = float(hitter_data['AB'] + hitter_data['BB'] + hitter_data['HBP'] + hitter_data['GDP'])
        TBF = float(pitcher_data['TBF'])
        HR = (((float(hitter_data['HR']) / PA) ** HITTER_WEIGHT) * ((float(pitcher_data['HR']) / TBF) ** PITCHER_WEIGHT)) ** (1.0 / float(HITTER_WEIGHT + PITCHER_WEIGHT))
        OneBase = (((float(hitter_data['H'] - hitter_data['2B'] - hitter_data['3B'] - hitter_data['HR'] + hitter_data['BB'] + hitter_data['HBP']) / PA) ** HITTER_WEIGHT) * ((float(pitcher_data['H'] - pitcher_data['2B'] - pitcher_data['3B'] - pitcher_data['HR'] + pitcher_data['BB'] + pitcher_data['HBP']) / TBF) ** PITCHER_WEIGHT)) ** (1.0 / float(HITTER_WEIGHT + PITCHER_WEIGHT))
        OneHit = (((float(hitter_data['H'] - hitter_data['2B'] - hitter_data['3B'] - hitter_data['HR']) / PA) ** HITTER_WEIGHT) * ((float(pitcher_data['H'] - pitcher_data['2B'] - pitcher_data['3B'] - pitcher_data['HR']) / TBF) ** PITCHER_WEIGHT)) ** (1.0 / float(HITTER_WEIGHT + PITCHER_WEIGHT))
        TwoHit = (((float(hitter_data['2B']) / PA) ** HITTER_WEIGHT) * ((float(pitcher_data['2B']) / TBF) ** PITCHER_WEIGHT)) ** (1.0 / float(HITTER_WEIGHT + PITCHER_WEIGHT))
        ThreeHit = (((float(hitter_data['3B']) / PA) ** HITTER_WEIGHT) * ((float(pitcher_data['3B']) / TBF) ** PITCHER_WEIGHT)) ** (1.0 / float(HITTER_WEIGHT + PITCHER_WEIGHT))
        BBHBP = (((float(hitter_data['BB'] + hitter_data['HBP']) / PA) ** HITTER_WEIGHT) * ((float(pitcher_data['BB'] + pitcher_data['HBP']) / TBF) ** PITCHER_WEIGHT)) ** (1.0 / float(HITTER_WEIGHT + PITCHER_WEIGHT))
        GDP = float(hitter_data['GDP']) / PA
        GTP = 692.0 / 14000000.0  # historically defined times of triple plays
        GSP = ((((float(hitter_data['AB'] + hitter_data['BB'] + hitter_data['HBP'] - hitter_data['H'] - GDP) / PA) ** HITTER_WEIGHT) * ((float(pitcher_data['TBF'] + pitcher_data['BB'] + pitcher_data['HBP'] - pitcher_data['H']) / PA) ** PITCHER_WEIGHT)) ** (1.0 / float(HITTER_WEIGHT + PITCHER_WEIGHT))) - GTP  # times of single plays

    # print(considered_data)

    A_data, B_data, C_data = [[0 for _ in range(64)] for _ in range(3)]
    # A_data
    # Column 0
    for row in range(8):
        A_data[8*row] = HR
    # Column 1
    A_data[1] = OneBase
    A_data[17] = OneHit
    A_data[25] = OneHit
    A_data[49] = OneHit
    # Column 2
    A_data[2] = TwoHit
    A_data[18] = TwoHit
    A_data[26] = TwoHit
    A_data[50] = TwoHit
    # Column 3
    for row in range(8):
        A_data[3 + 8*row] = ThreeHit
    # Column 4
    A_data[12] = BBHBP
    A_data[20] = BBHBP
    A_data[36] = OneHit
    A_data[44] = OneHit
    A_data[60] = OneHit
    # Column 5
    A_data[29] = BBHBP
    # Column 6
    A_data[14] = TwoHit
    A_data[38] = TwoHit
    A_data[46] = TwoHit
    A_data[62] = TwoHit
    # Column 7
    A_data[39] = BBHBP
    A_data[47] = BBHBP
    A_data[55] = BBHBP
    A_data[63] = BBHBP

    # B_data
    for i in range(8):
        B_data[i + 8*i] = GSP

    # C_data
    C_data[8] = GDP
    C_data[16] = GDP
    C_data[24] = GDP

    # D_data
    D_data = [0, 0, 0, 0, GTP, GTP, GTP, GTP]

    # E_data
    E_data = [0, GDP, GDP, GDP, GDP, GDP, GDP, GDP]

    #F_data
    F_scalar = GSP + GDP  # at 2-outs, a double-play possible play still yields a single out
    F_data = [F_scalar for _ in range(8)]

    A = Matrix(8, 8, A_data)
    B = Matrix(8, 8, B_data)
    C = Matrix(8, 8, C_data)
    D = Matrix(8, 1, D_data)
    E = Matrix(8, 1, E_data)
    F = Matrix(8, 1, F_data)

    P_0 = matrix_augment(A, B, C, D)
    P_1 = matrix_augment(zero_matrix, A, B, E)
    P_2 = matrix_augment(zero_matrix, zero_matrix, A, F)
    P_3 = matrix_augment(zero_row, one_matrix)
    P = matrix_augment(P_0, P_1, P_2, P_3, horizontally=False)
    # P.print()
    P.normalize(sum_to=1.0)
    # P.print()

    ###
    for row_count in range(8):
        row_temp = P.get_row_data(row_count)
        row_sum = sum(row_temp)
        difference = 1 - row_sum
        P.insert(difference + P.store[row_count][0], row_count, 0)
    for row_count in range(8, 25):
        row_temp = P.get_row_data(row_count)
        row_sum = sum(row_temp)
        difference = 1 - row_sum
        P.insert(difference + P.store[row_count][24], row_count, 24)
    ###

    A0_data = P.get_block_data(0, 0, 7, 7, linearize=True)
    A1_data = P.get_block_data(8, 8, 15, 15, linearize=True)
    A2_data = P.get_block_data(16, 16, 23, 23, linearize=True)
    B0_data = P.get_block_data(0, 8, 7, 15, linearize=True)
    B1_data = P.get_block_data(8, 16, 15, 23, linearize=True)
    C0_data = P.get_block_data(0, 16, 7, 23, linearize=True)
    D0_data = P.get_block_data(0, 24, 7, 24, linearize=True)
    E1_data = P.get_block_data(8, 24, 15, 24, linearize=True)
    F2_data = P.get_block_data(16, 24, 23, 24, linearize=True)

    R0 = [1, 2, 3, 4, 5, 6, 7, 12, 13, 14, 15, 20, 21, 22, 23, 28, 29, 30, 31, 39, 47, 55]
    R1 = [0, 9, 10, 11, 17, 18, 19, 25, 26, 27, 36, 37, 38, 44, 45, 46, 52, 53, 54, 63]
    R2 = [8, 16, 24, 33, 34, 35, 41, 42, 43, 49, 50, 51]
    R3 = [32, 40, 48, 57, 58, 59]
    R4 = [56]

    A0_data_list = [[0 for _ in range(64)] for _ in range(5)]
    A1_data_list = [[0 for _ in range(64)] for _ in range(5)]
    A2_data_list = [[0 for _ in range(64)] for _ in range(5)]

    A__data = [A0_data, A1_data, A2_data]
    A__data_list = [A0_data_list, A1_data_list, A2_data_list]
    for i in range(3):
        for r in R0:
            A__data_list[i][0][r] = A__data[i][r]
        for r in R1:
            A__data_list[i][1][r] = A__data[i][r]
        for r in R2:
            A__data_list[i][2][r] = A__data[i][r]
        for r in R3:
            A__data_list[i][3][r] = A__data[i][r]
        for r in R4:
            A__data_list[i][4][r] = A__data[i][r]

    P0_0 = matrix_augment(Matrix(8, 8, A__data_list[0][0]), Matrix(8, 8, B0_data), Matrix(8, 8, C0_data), Matrix(8, 1, D0_data))
    P0_1 = matrix_augment(zero_matrix, Matrix(8, 8, A__data_list[1][0]), Matrix(8, 8, B1_data), Matrix(8, 1, E1_data))
    P0_2 = matrix_augment(zero_matrix, zero_matrix, Matrix(8, 8, A__data_list[2][0]), Matrix(8, 1, F2_data))
    P0_3 = matrix_augment(zero_row, one_matrix)
    P0 = matrix_augment(P0_0, P0_1, P0_2, P0_3, horizontally=False)

    P1_0 = matrix_augment(Matrix(8, 8, A__data_list[0][1]), zero_matrix, zero_matrix, zero_column)
    P1_1 = matrix_augment(zero_matrix, Matrix(8, 8, A__data_list[1][1]), zero_matrix, zero_column)
    P1_2 = matrix_augment(zero_matrix, zero_matrix, Matrix(8, 8, A__data_list[2][1]), zero_column)
    P1_3 = matrix_augment(zero_row, Matrix(1, 1, [0]))
    P1 = matrix_augment(P1_0, P1_1, P1_2, P1_3, horizontally=False)

    P2_0 = matrix_augment(Matrix(8, 8, A__data_list[0][2]), zero_matrix, zero_matrix, zero_column)
    P2_1 = matrix_augment(zero_matrix, Matrix(8, 8, A__data_list[1][2]), zero_matrix, zero_column)
    P2_2 = matrix_augment(zero_matrix, zero_matrix, Matrix(8, 8, A__data_list[2][2]), zero_column)
    P2_3 = matrix_augment(zero_row, Matrix(1, 1, [0]))
    P2 = matrix_augment(P2_0, P2_1, P2_2, P2_3, horizontally=False)

    P3_0 = matrix_augment(Matrix(8, 8, A__data_list[0][3]), zero_matrix, zero_matrix, zero_column)
    P3_1 = matrix_augment(zero_matrix, Matrix(8, 8, A__data_list[1][3]), zero_matrix, zero_column)
    P3_2 = matrix_augment(zero_matrix, zero_matrix, Matrix(8, 8, A__data_list[2][3]), zero_column)
    P3_3 = matrix_augment(zero_row, Matrix(1, 1, [0]))
    P3 = matrix_augment(P3_0, P3_1, P3_2, P3_3, horizontally=False)

    P4_0 = matrix_augment(Matrix(8, 8, A__data_list[0][4]), zero_matrix, zero_matrix, zero_column)
    P4_1 = matrix_augment(zero_matrix, Matrix(8, 8, A__data_list[1][4]), zero_matrix, zero_column)
    P4_2 = matrix_augment(zero_matrix, zero_matrix, Matrix(8, 8, A__data_list[2][4]), zero_column)
    P4_3 = matrix_augment(zero_row, Matrix(1, 1, [0]))
    P4 = matrix_augment(P4_0, P4_1, P4_2, P4_3, horizontally=False)

    return [P0, P1, P2, P3, P4, P]


def normalize_list(data, sum_to=1):
    data_sum = sum(data)
    return [float(sum_to) * float(elem) / float(data_sum) for elem in data]


def convolute_probability_vectors(*args):
    def convolute_probability_vectors_basic(A, B):
        if len(A) != len(B):
            return False
        convolution = [0.0 for _ in range(len(A))]
        for i in range(len(A)):
            for j in range(len(B) - i):
                convolution[i+j] += A[i] * B[j]
        return convolution
    if len(args) < 2:
        return False
    convolution = args[0]
    for vector in args[1:]:
        if convolution is False:
            return False
        convolution = convolute_probability_vectors_basic(convolution, vector)
    return convolution


def single_inning_run_distribution(hitter_lineup, index, threshold=0.03, pitcher_id=None, consider='0010'):
    # TODO: the threshold converges to about 0.2299... and no lower -> fix this such that it can converge to 0
    ADJUSTED_THRESHOLD = 0.001
    initial_index = index
    transition_matrices = [generate_transition_matrix(hitter_id=hitter_id, pitcher_id=pitcher_id, consider=consider) for hitter_id in hitter_lineup]
    U = Matrix(21, 25)
    U.insert(1, 0, 0)
    counter = 0

    while abs(sum(U.get_col_data(24)) - 1) > threshold:
        if counter == 50:
            break
        # print("1st difference:", abs(sum(U.get_col_data(24)) - 1))
        index = index % len(hitter_lineup)
        P0, P1, P2, P3, P4, P = transition_matrices[index]
        temp_matrix = Matrix(21, 25)
        for row in range(20):
            row_temp = Matrix(1, 25, U.get_row_data(row)) * P0
            if row > 0:
                row_temp += Matrix(1, 25, U.get_row_data(row - 1)) * P1
            if row > 1:
                row_temp += Matrix(1, 25, U.get_row_data(row - 2)) * P2
            if row > 2:
                row_temp += Matrix(1, 25, U.get_row_data(row - 3)) * P3
            if row > 3:
                row_temp += Matrix(1, 25, U.get_row_data(row - 4)) * P4
            temp_matrix.set_row_data(row, row_temp.get_store_data())
        U = temp_matrix
        index += 1
        counter += 1

    if counter < 50:
        print("No recalculation required")
        return normalize_list(U.get_col_data(24)), index

    # redo the step above
    print("Threshold recalculating...")
    threshold = abs(sum(U.get_col_data(24)) - 1) + ADJUSTED_THRESHOLD
    U = Matrix(21, 25)
    U.insert(1, 0, 0)
    counter = 0
    index = initial_index

    while abs(sum(U.get_col_data(24)) - 1) > threshold:
        # print("2nd difference:", abs(sum(U.get_col_data(24)) - 1))
        index = index % len(hitter_lineup)
        P0, P1, P2, P3, P4, P = transition_matrices[index]
        temp_matrix = Matrix(21, 25)
        for row in range(20):
            row_temp = Matrix(1, 25, U.get_row_data(row)) * P0
            if row > 0:
                row_temp += Matrix(1, 25, U.get_row_data(row - 1)) * P1
            if row > 1:
                row_temp += Matrix(1, 25, U.get_row_data(row - 2)) * P2
            if row > 2:
                row_temp += Matrix(1, 25, U.get_row_data(row - 3)) * P3
            if row > 3:
                row_temp += Matrix(1, 25, U.get_row_data(row - 4)) * P4
            temp_matrix.set_row_data(row, row_temp.get_store_data())
        U = temp_matrix
        index += 1
        counter += 1

    # print("Counter: " + str(counter))
    print("Threshold: " + str(threshold))
    return normalize_list(U.get_col_data(24)), index


def nine_inning_run_distribution(hitter_lineup, pitcher_id=None, consider='0010', threshold=0.03):
    distributions = []
    index = 0
    for inning in range(9):
        distribution, index = single_inning_run_distribution(hitter_lineup, index, pitcher_id=pitcher_id, consider=consider, threshold=threshold)
        distributions.append(distribution)
    return convolute_probability_vectors(*distributions)


def expected_run(hitter_lineup, pitcher_id=None, consider='0010', threshold=0.03):
    run = 0.0
    run_distribution = nine_inning_run_distribution(hitter_lineup, pitcher_id=pitcher_id, consider=consider, threshold=threshold)
    for i in range(len(run_distribution)):
        run += i * run_distribution[i]
    return run


def get_total_data(player_id, player_type):
    # Note: df['연도'] can be checked if it is NaN by using pd.isna(obj) function (returns True if obj is NaN)
    # TODO: return an alternative data (i.e. average of the team or the league) for a new player who has no total data
    df = pd.read_csv("/Volumes/Samsung_T5/KBO_Data/Players/" + str(player_id) + "/" + str(player_id) + "_" + player_type.lower() + "_total_regular_season.csv")
    last_row = df.values.tolist()[-1]
    header = list(df)
    total_data = dict()
    for i in range(len(header)):
        total_data[header[i]] = last_row[i]
    return total_data


def get_current_data(player_id, player_type, year=2019):
    current_data = dict()
    if player_type == "Hitter":
        df = pd.read_csv("/Volumes/Samsung_T5/KBO_Data/Players/" + str(player_id) + "/" + str(player_id) + "_hitter_total_regular_season.csv")
        current_row = []
        try:
            current_row = df.loc[df['연도'] == 2019].values.tolist()[0]
        except KeyError:
            print(player_type + " data in " + str(year) + " for player " + str(player_id) + " does not exist.")
            current_row = get_total_data(player_id, player_type)
        header = list(df)
        for i in range(len(header)):
            current_data[header[i]] = current_row[i]
    elif player_type == "Pitcher":
        df_TBF = pd.read_csv("/Volumes/Samsung_T5/KBO_Data/Players/" + str(player_id) + "/" + str(player_id) + "_pitcher_total_regular_season.csv")
        TBF = df_TBF.loc[df_TBF['연도'] == 2019]['TBF'].values[0]
        df = pd.read_csv("/Volumes/Samsung_T5/KBO_Data/Players/" + str(player_id) + "/" + str(player_id) + "_Situation/" + str(player_id) + "_pitcher_타자유형별_" + str(year) + "_regular_season.csv")
        header = list(df)[1:]
        left_row = df.loc[df['구분'] == '좌타자'].values.tolist()[0][1:]
        right_row = df.loc[df['구분'] == '우타자'].values.tolist()[0][1:]
        for i in range(len(header)):
            current_data[header[i]] = left_row[i] + right_row[i]
        current_data['TBF'] = TBF
    return current_data


def get_player_id_dict(id_as_key=False, file_name='kbo_id_list.csv'):
    df = pd.read_csv(file_name)[['ID', 'Name']].values.tolist()
    id_dict = dict()
    for row in df:
        if id_as_key:
            id_dict[int(row[0])] = row[1]
        if not id_as_key:
            key = row[1]  # name of the player
            if key not in id_dict:
                id_dict[key] = [int(row[0])]
            else:
                id_dict[key].append(int(row[0]))
    return id_dict


def find_player_id(player_name, team_name=None, number=None, position=None, birth_year=None, file_name='kbo_id_list.csv'):
    id_df = pd.read_csv(file_name)
    id_df = id_df.loc[(id_df['Name'] == player_name) & ((id_df['Team'] == team_name) | (team_name == None)) & ((id_df['Number'] == number) | (number == None)) & ((id_df['Position'] == position) | (position == None)) & ((id_df['Birth Year'] == birth_year) | (birth_year == None))]
    # print(id_df)
    if id_df.shape[0] > 1:
        print("More data filtration required for: " + player_name)
        return False
    return id_df.loc[:, 'ID'].values.tolist()[0]


def sort_string_list_by_length(str_list):
    return sorted(str_list, key=len, reverse=True)


if __name__ == '__main__':
    samsung_hitter_lineup = [find_player_id(player_name='박해민', team_name='삼성 라이온즈'),
                             find_player_id(player_name='김성훈', team_name='삼성 라이온즈'),
                             find_player_id(player_name='구자욱', team_name='삼성 라이온즈'),
                             find_player_id(player_name='러프', team_name='삼성 라이온즈'),
                             find_player_id(player_name='이학주', team_name='삼성 라이온즈'),
                             find_player_id(player_name='최영진', team_name='삼성 라이온즈'),
                             find_player_id(player_name='백승민', team_name='삼성 라이온즈'),
                             find_player_id(player_name='김헌곤', team_name='삼성 라이온즈'),
                             find_player_id(player_name='김도환', team_name='삼성 라이온즈')]
    kiwoom_hitter_lineup = [find_player_id(player_name='이정후', team_name='키움 히어로즈'),
                            find_player_id(player_name='김하성', team_name='키움 히어로즈'),
                            find_player_id(player_name='샌즈', team_name='키움 히어로즈'),
                            find_player_id(player_name='박병호', team_name='키움 히어로즈'),
                            find_player_id(player_name='서건창', team_name='키움 히어로즈'),
                            find_player_id(player_name='장영석', team_name='키움 히어로즈'),
                            find_player_id(player_name='임병욱', team_name='키움 히어로즈'),
                            find_player_id(player_name='김혜성', team_name='키움 히어로즈'),
                            find_player_id(player_name='이지영', team_name='키움 히어로즈')]
    hanwha_hitter_lineup = [find_player_id(player_name='정은원', team_name='한화 이글스'),
                            find_player_id(player_name='오선진', team_name='한화 이글스'),
                            find_player_id(player_name='호잉', team_name='한화 이글스'),
                            find_player_id(player_name='이성열', team_name='한화 이글스'),
                            find_player_id(player_name='송광민', team_name='한화 이글스'),
                            find_player_id(player_name='김태균', team_name='한화 이글스'),
                            find_player_id(player_name='최진행', team_name='한화 이글스'),
                            find_player_id(player_name='최재훈', team_name='한화 이글스'),
                            find_player_id(player_name='장진혁', team_name='한화 이글스')]
    doosan_hitter_lineup = [find_player_id(player_name='정수빈', team_name='두산 베어스'),
                            find_player_id(player_name='류지혁', team_name='두산 베어스'),
                            find_player_id(player_name='페르난데스', team_name='두산 베어스'),
                            find_player_id(player_name='김재환', team_name='두산 베어스'),
                            find_player_id(player_name='박건우', team_name='두산 베어스'),
                            find_player_id(player_name='박세혁', team_name='두산 베어스'),
                            find_player_id(player_name='오재일', team_name='두산 베어스'),
                            find_player_id(player_name='허경민', team_name='두산 베어스'),
                            find_player_id(player_name='김재호', team_name='두산 베어스')]
    kia_hitter_lineup = [find_player_id(player_name='이명기', team_name='KIA 타이거즈'),
                         find_player_id(player_name='김선빈', team_name='KIA 타이거즈'),
                         find_player_id(player_name='안치홍', team_name='KIA 타이거즈'),
                         find_player_id(player_name='최형우', team_name='KIA 타이거즈'),
                         find_player_id(player_name='김주찬', team_name='KIA 타이거즈'),
                         find_player_id(player_name='이창진', team_name='KIA 타이거즈'),
                         find_player_id(player_name='오선우', team_name='KIA 타이거즈'),
                         find_player_id(player_name='박찬호', team_name='KIA 타이거즈'),
                         find_player_id(player_name='한승택', team_name='KIA 타이거즈')]
    lg_hitter_lineup = [find_player_id(player_name='이천웅', team_name='LG 트윈스'),
                        find_player_id(player_name='박용택', team_name='LG 트윈스'),
                        find_player_id(player_name='김현수', team_name='LG 트윈스'),
                        find_player_id(player_name='채은성', team_name='LG 트윈스'),
                        find_player_id(player_name='이형종', team_name='LG 트윈스'),
                        find_player_id(player_name='오지환', team_name='LG 트윈스'),
                        find_player_id(player_name='김민성', team_name='LG 트윈스'),
                        find_player_id(player_name='유강남', team_name='LG 트윈스'),
                        find_player_id(player_name='박지규', team_name='LG 트윈스')]
    lotte_hitter_lineup = [find_player_id(player_name='아수아헤', team_name='롯데 자이언츠'),
                           find_player_id(player_name='민병헌', team_name='롯데 자이언츠'),
                           find_player_id(player_name='손아섭', team_name='롯데 자이언츠'),
                           find_player_id(player_name='이대호', team_name='롯데 자이언츠'),
                           find_player_id(player_name='전준우', team_name='롯데 자이언츠'),
                           find_player_id(player_name='채태인', team_name='롯데 자이언츠'),
                           find_player_id(player_name='신본기', team_name='롯데 자이언츠'),
                           find_player_id(player_name='강로한', team_name='롯데 자이언츠'),
                           find_player_id(player_name='나종덕', team_name='롯데 자이언츠')]
    nc_hitter_lineup = [find_player_id(player_name='이상호', team_name='NC 다이노스'),
                        find_player_id(player_name='김태진', team_name='NC 다이노스', position='Infielder'),
                        find_player_id(player_name='박석민', team_name='NC 다이노스'),
                        find_player_id(player_name='양의지', team_name='NC 다이노스'),
                        find_player_id(player_name='이원재', team_name='NC 다이노스'),
                        find_player_id(player_name='베탄코트', team_name='NC 다이노스'),
                        find_player_id(player_name='권희동', team_name='NC 다이노스'),
                        find_player_id(player_name='김성욱', team_name='NC 다이노스'),
                        find_player_id(player_name='김찬형', team_name='NC 다이노스')]
    sk_hitter_lineup = [find_player_id(player_name='김재현', team_name='SK 와이번스'),
                        find_player_id(player_name='한동민', team_name='SK 와이번스'),
                        find_player_id(player_name='최정', team_name='SK 와이번스'),
                        find_player_id(player_name='로맥', team_name='SK 와이번스'),
                        find_player_id(player_name='고종욱', team_name='SK 와이번스'),
                        find_player_id(player_name='이재원', team_name='SK 와이번스'),
                        find_player_id(player_name='배영섭', team_name='SK 와이번스'),
                        find_player_id(player_name='김성현', team_name='SK 와이번스'),
                        find_player_id(player_name='정현', team_name='SK 와이번스')]
    kt_hitter_lineup = [find_player_id(player_name='김민혁', team_name='KT 위즈'),
                        find_player_id(player_name='오태곤', team_name='KT 위즈'),
                        find_player_id(player_name='강백호', team_name='KT 위즈'),
                        find_player_id(player_name='로하스', team_name='KT 위즈'),
                        find_player_id(player_name='유한준', team_name='KT 위즈'),
                        find_player_id(player_name='황재균', team_name='KT 위즈'),
                        find_player_id(player_name='박경수', team_name='KT 위즈'),
                        find_player_id(player_name='장성우', team_name='KT 위즈'),
                        find_player_id(player_name='심우준', team_name='KT 위즈')]

    # collect_kbo_player_data("Hitter", "Situation", custom_id_list=kt_hitter_lineup)
    # collect_kbo_player_data("Hitter", "Total", custom_id_list=kt_hitter_lineup)
    # collect_kbo_player_data("Hitter", "Situation", custom_id_list=kia_hitter_lineup)
    # collect_kbo_player_data("Hitter", "Total", custom_id_list=kia_hitter_lineup)
    # collect_kbo_player_data("Pitcher", "Situation", custom_id_list=[find_player_id(player_name='김민', team_name='KT 위즈'), find_player_id(player_name='윌랜드', team_name='KIA 타이거즈')])
    # collect_kbo_player_data("Pitcher", "Total", custom_id_list=[find_player_id(player_name='김민', team_name='KT 위즈'), find_player_id(player_name='윌랜드', team_name='KIA 타이거즈')])

    # collect_kbo_player_data("Pitcher", "Situation", custom_id_list=[find_player_id(player_name='윌슨', team_name='LG 트윈스'), find_player_id(player_name='서준원', team_name='롯데 자이언츠')])
    # collect_kbo_player_data("Pitcher", "Total", custom_id_list=[find_player_id(player_name='윌슨', team_name='LG 트윈스'), find_player_id(player_name='서준원', team_name='롯데 자이언츠')])

    # print(expected_run(kia_hitter_lineup, pitcher_id=find_player_id(player_name='김민', team_name='KT 위즈'), consider='0011', threshold=0.001))
    # print(expected_run(kt_hitter_lineup, pitcher_id=find_player_id(player_name='윌랜드', team_name='KIA 타이거즈'), consider='0011', threshold=0.001))

    print(find_player_id(player_name='조한욱'))
    print(find_player_id(player_name='오준혁'))
    print(find_player_id(player_name='박승욱'))
