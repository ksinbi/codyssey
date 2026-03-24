def read_csv_file(filename):
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            next(file)  # 헤더 제거
            for line in file:
                parts = line.strip().split(',')

                # 🔥 Various 포함된 행 제거
                if "Various" in parts:
                    continue

                try:
                    item = {
                        'Substance': parts[0],
                        'Weight': parts[1],
                        'Specific Gravity': parts[2],
                        'Strength': parts[3],
                        'Flammability': float(parts[4])
                    }
                    data.append(item)
                except (ValueError, IndexError):
                    continue

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
    except Exception as e:
        print("파일 읽기 오류:", e)

    return data


def print_data(data, title):
    print(f"\n[{title}]")

    # 🔥 위험 물질일 때
    if "위험 물질" in title:
        print(f"{'물질명':<20} {'인화성':<10}")
        print("-" * 30)
        for item in data:
            print(f"{item['Substance']:<20} {item['Flammability']:<10}")

    # 🔥 전체 데이터 출력
    else:
        print(f"{'물질명':<20} {'밀도(g/cm³)':<15} {'비중':<10} {'강도':<15} {'인화성':<10}")
        print("-" * 75)
        for item in data:
            print(f"{item['Substance']:<20} {item['Weight']:<15} {item['Specific Gravity']:<10} {item['Strength']:<15} {item['Flammability']:<10}")

def sort_by_flammability(data):
    return sorted(data, key=lambda x: x['Flammability'], reverse=True)


def filter_dangerous(data):
    return [item for item in data if item['Flammability'] >= 0.7]


def save_csv(filename, data):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("Substance,Weight,Specific Gravity,Strength,Flammability\n")
            for item in data:
                file.write(f"{item['Substance']},{item['Weight']},{item['Specific Gravity']},{item['Strength']},{item['Flammability']}\n")
    except Exception as e:
        print("CSV 저장 오류:", e)


def save_binary(filename, data):
    try:
        with open(filename, 'wb') as file:
            for item in data:
                line = f"{item['Substance']},{item['Weight']},{item['Specific Gravity']},{item['Strength']},{item['Flammability']}\n"
                file.write(line.encode('utf-8'))
    except Exception as e:
        print("이진 파일 저장 오류:", e)


def load_binary(filename):
    data = []
    try:
        with open(filename, 'rb') as file:
            for line in file:
                decoded = line.decode('utf-8').strip()
                parts = decoded.split(',')

                item = {
                    'Substance': parts[0],
                    'Weight': parts[1],
                    'Specific Gravity': parts[2],
                    'Strength': parts[3],
                    'Flammability': float(parts[4])
                }
                data.append(item)

    except Exception as e:
        print("이진 파일 읽기 오류:", e)

    return data


# ================= 실행 =================
def main():
    filename = "Mars_Base_Inventory_List.csv"

    data = read_csv_file(filename)
    print_data(data, "원본 데이터")

    sorted_data = sort_by_flammability(data)
    print_data(sorted_data, "인화성 기준 정렬")

    danger_data = filter_dangerous(sorted_data)
    print_data(danger_data, "위험 물질 (0.7 이상)")

    save_csv("Mars_Base_Inventory_danger.csv", danger_data)

    save_binary("Mars_Base_Inventory_List.bin", sorted_data)

    loaded_bin = load_binary("Mars_Base_Inventory_List.bin")
    print_data(loaded_bin, "이진 파일에서 읽은 데이터")


if __name__ == "__main__":
    main()