import copy

def get_matrix_input(size):
    """n*n 행렬 입력받기"""
    matrix = []
    print(f"\n{size}x{size} 행렬의 원소를 한 줄에 하나씩 입력하세요.")
    for i in range(size):
        while True:
            try:
                row = list(map(float, input(f"{i+1}번째 행 입력: ").split()))
                if len(row) == size:
                    matrix.append(row)
                    break
                else:
                    print(f"오류: {size}개의 원소를 입력해야 합니다.")
            except ValueError:
                print("오류: 숫자를 입력해주세요.")
    return matrix

#행렬 출력
def print_matrix(m, title=""):
  if not m or not m[0]:
    print("없음")
    return
  print(f"\n{title}")
  col_widths = [max(len(f"{item:.4f}") for item in col) for col in zip(*m)]
    
  for row in m:
      for i, item in enumerate(row):          
         print(f"{item:<{col_widths[i] + 2}.4f}", end="")
      print()
  print("-" * (sum(col_widths) + 2 * len(col_widths)))

#전치행렬 구하기   
def transposeMatrix(m):
  return[[m[j][i] for j in range(len(m))]for i in range(len(m[0]))]

def getMatrixMinor(m, i, j):
  return [row[:j]+row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeterminant(m):
  if len(m)==1:
    return m[0][0]
  if(len(m)==2):
    return m[0][0]*m[1][1] - m[1][0]*m[0][1]
  
  determinant = 0
  for c in range(len(m)):
    determinant += ((-1)**c)*m[0][c] * getMatrixDeterminant(getMatrixMinor(m,0,c))

  return determinant


def getMatrixInverse(m):
    determinant = getMatrixDeterminant(m)
    
    # 행렬식 값이 0이면 역행렬이 없으므로 None 반환
    if abs(determinant) < 1e-9:
        return None

    if len(m)==1:
        return[[1.0/m[0][0]]]
    if len(m)==2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]
    
    cofactors=[]
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c))*getMatrixDeterminant(minor))
        cofactors.append(cofactorRow)

    adjugate = transposeMatrix(cofactors)

    for r in range(len(adjugate)):
        for c in range(len(adjugate)):
            adjugate[r][c] = adjugate[r][c]/determinant

    return adjugate

#가우스-조던 소거법
def inverse_gauss_jordan(m):
  n = len(m)
  matrix = copy.deepcopy(m)

  identity = [[float(i==j) for i in range(n)]for j in range(n)]

  for i in range(n):
    pivot = i
    while pivot < n and abs(matrix[pivot][i])<1e-9:
      pivot +=1
    
    if(pivot == n):
      return None
    
    #pivot행과 i행 교환
    matrix[i],matrix[pivot] = matrix[pivot], matrix[i]
    identity[i], identity[pivot] = identity[pivot],identity[i]

    #대각원소1
    divisor = matrix[i][i]
    for j in range(i,n):
      matrix[i][j] /= divisor
    for j in range(n):
      identity[i][j] /=divisor

    #i열 나머지 원소 0
    for row in range(n):
      if row != i:
        multiplier = matrix[row][i]
        for col in range(i,n):
          matrix[row][col] -= multiplier * matrix[i][col]
        for col in range(n):
          identity[row][col]-=multiplier * identity[i][col]

  return identity

#결과 비교
def compare(m1,m2,tolerance = 1e-9):
  if not m1 or not m2 or len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
    return False
  for i in range(len(m1)):
    for j in range(len(m1[0])):
      if abs(m1[i][j]-m2[i][j]) > tolerance:
        return False
  return True

def main():
    try:
        n = int(input("정방행렬의 차수를 입력하시오: "))
        if n<=0:
            print("차수는 양의 정수여야 함")
            return
        matrix = get_matrix_input(n)
        print_matrix(matrix,"입력된 행렬")

        #행렬식계산
        inv_det = getMatrixInverse(matrix)

        #가우스계산
        inv_gj = inverse_gauss_jordan(matrix)

        if inv_det is None or inv_gj is None:
            # 수정된 오류 메시지
            print("\n[결과] 입력된 행렬의 역행렬은 존재하지 않습니다. (행렬식 값이 0입니다)")
        else:
            print_matrix(inv_det, "행렬식 역행렬")
            print_matrix(inv_gj, "가우스-조던 소거법 역행렬")

            print("\n결과 비교")
            if compare(inv_det, inv_gj):
                print("역행렬이 동일함")
            else :
                print("역행렬이 다름")
    except ValueError:
        print("정수를 입력하세요")
    except Exception as e:
        print(f"알 수 없는 오류가 발생함: {e}")
if __name__ == "__main__":
  main()