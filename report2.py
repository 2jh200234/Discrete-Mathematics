import copy

def get_relation_matrix(size):
    matrix = []
    print(f"각 행의 원소 5개를 0 또는 1로, 띄어쓰기로 구분하여 입력하세요.")
    
    for i in range(size):
        while True:
            try:
                # 입력을 받아 공백으로 분리 후 정수로 변환
                row_input = input(f"{i+1}번째 행 입력: ").split()
                row = list(map(int, row_input))
                
                # 원소 개수 확인
                if len(row) != size:
                    print(f"오류: {size}개의 원소를 입력하세요. (현재 {len(row)}개)")
                    continue
                
                # 원소가 0 또는 1인지 확인
                if not all(x in [0, 1] for x in row):
                    print(f"오류: 원소는 0 또는 1이어야 합니다.")
                    continue
                    
                matrix.append(row)
                break  # 올바른 입력이므로 다음 행으로 넘어감
                
            except ValueError:
                print("오류: 숫자를 입력해주세요.")
            except Exception as e:
                print(f"알 수 없는 오류: {e}")
                
    return matrix

def print_matrix(matrix, title=""):
    """
    주어진 행렬 출력
    """
    print(f"\n--- {title} ---")
    if not matrix or not matrix[0]:
        print("[] (빈 행렬)")
        return
    
    for row in matrix:
        # 각 원소를 문자열로 변환하여 공백으로 연결
        print(" ".join(map(str, row)))
    print("-" * (len(title) + 6))


# --- 2. 동치 관계 판별 기능 (개별 함수) ---

def is_reflexive(matrix, size):
    """
    반사성 확인
    """
    for i in range(size):
        if matrix[i][i] == 0:
            print(f"반사성(X): M[{i+1}][{i+1}]이 0입니다.")
            return False
    print("반사성(O): 모든 주 대각선 원소가 1입니다.")
    return True

def is_symmetric(matrix, size):
    """
    대칭성 확인
    """
    for i in range(size):
        for j in range(i + 1, size):
            if matrix[i][j] != matrix[j][i]:
                print(f"대칭성(X): M[{i+1}][{j+1}] != M[{j+1}][{i+1}]")
                return False
    print("대칭성(O): 모든 M[i][j]가 M[j][i]와 같습니다.")
    return True

def is_transitive(matrix, size):
    """
    추이성 확인
    """
    for i in range(size):
        for j in range(size):
            for k in range(size):
                if matrix[i][j] == 1 and matrix[j][k] == 1:
                    if matrix[i][k] == 0:
                        print(f"추이성(X): M[{i+1}][{j+1}]=1, M[{j+1}][{k+1}]=1 이지만 M[{i+1}][{k+1}]=0 입니다.")
                        return False
    print("추이성(O): 만족합니다.")
    return True

# --- 3. 동치류 출력 기능 ---

def get_equivalence_classes(matrix, size):
    print("\n--- 동치류 계산 (Equivalence Classes) ---")
    
    
    for i in range(size):            
        current_class = []
        for j in range(size):
            if matrix[i][j] == 1:
                current_class.append(j + 1)
        
        # 각 원소(i+1)의 동치류를 항상 출력
        print(f"  [{i + 1}]의 동치류 = {set(current_class)}")

# --- 4. 폐포 구현 기능 ---

def get_reflexive_closure(matrix, size):
    """ 반사 폐포를 구합니다. """
    closure = copy.deepcopy(matrix)
    for i in range(size):
        closure[i][i] = 1
    return closure

def get_symmetric_closure(matrix, size):
    """ 대칭 폐포를 구합니다. """
    closure = copy.deepcopy(matrix)
    for i in range(size):
        for j in range(i + 1, size):
            if closure[i][j] == 1 or closure[j][i] == 1:
                closure[i][j] = 1
                closure[j][i] = 1
    return closure

def get_transitive_closure(matrix, size):
    """추이 폐포를 구합니다. (Warshall's Algorithm) """
    closure = copy.deepcopy(matrix)
    for k in range(size): 
        for i in range(size): 
            for j in range(size): 
                closure[i][j] = closure[i][j] or (closure[i][k] and closure[k][j])
    return closure


def analyze_matrix_properties(matrix, size, title):
    print(f"\n======================================")
    print(f"--- [ {title} ]에 대한 관계 성질 판별 ---")
    print(f"======================================")
    
    # 분석 대상 행렬을 먼저 출력
    print_matrix(matrix, f"{title} (M)")

    # 3가지 성질을 모두 검사
    is_ref = is_reflexive(matrix, size)
    is_sym = is_symmetric(matrix, size)
    is_trans = is_transitive(matrix, size)
    print("---------------------------------")

    # 최종 결론
    if is_ref and is_sym and is_trans:
        print(f"\n[최종 결론] [ {title} ]은(는) 동치 관계입니다.")
        # 동치 관계이므로 동치류 계산
        get_equivalence_classes(matrix, size)
    else:
        print(f"\n[최종 결론] [ {title} ]은(는) 동치 관계가 아닙니다.")
    
    # 원본 행렬의 성질 판별 결과를 반환 (폐포 생성 여부 결정용)
    return (is_ref, is_sym, is_trans)

# --- 메인 실행 함수 ---

def main():
    try:
        MATRIX_SIZE = 5  
        
        original_matrix = get_relation_matrix(MATRIX_SIZE)
        
        (is_ref, is_sym, is_trans) = analyze_matrix_properties(
            original_matrix, MATRIX_SIZE, "원본 행렬"
        )

        if not (is_ref and is_sym and is_trans):
            print("\n\n==============================================")
            print("--- 폐포 분석 ---")
            print("==============================================")

            if not is_ref:
                print_matrix(original_matrix, "원본 행렬 (비교용)")
                r_closure = get_reflexive_closure(original_matrix, MATRIX_SIZE)
                analyze_matrix_properties(r_closure, MATRIX_SIZE, "반사 폐포")
            
            if not is_sym:
                print_matrix(original_matrix, "원본 행렬 (비교용)")
                s_closure = get_symmetric_closure(original_matrix, MATRIX_SIZE)
                analyze_matrix_properties(s_closure, MATRIX_SIZE, "대칭 폐포")

            if not is_trans:
                print_matrix(original_matrix, "원본 행렬 (비교용)")
                t_closure = get_transitive_closure(original_matrix, MATRIX_SIZE)
                analyze_matrix_properties(t_closure, MATRIX_SIZE, "추이 폐포")

    except Exception as e:
        print(f"\n프로그램 실행 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()