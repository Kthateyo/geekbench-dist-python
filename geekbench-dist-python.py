import db, chart, sys, web


def main():
    singles = []
    multies = []
    cpu_names = []

    for i in range(1, len(sys.argv)):
        cpu_name = sys.argv[i]
        cpu_names.append(cpu_name)

        # DEBUG 
        print(f"CPU {i}/{len(sys.argv)-1} :", cpu_name)

        if not db.is_table_exist(cpu_name):
            data = web.scrap_data(cpu_name)

            db.create_table(cpu_name)
            db.insert_rows(cpu_name, data)

        singles.append(db.get_table_column(cpu_name, "single_core_score"))
        multies.append(db.get_table_column(cpu_name, "multi_core_score"))

    print("Drawing Plot...")
    chart.kde(cpu_names, singles, multies)


if __name__ == "__main__":
    main()
