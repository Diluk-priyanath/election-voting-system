import mysql.connector


def create_database(cursor):
    cursor.execute("CREATE DATABASE IF NOT EXISTS election")



def home():
    print("\n\n\t\t\t\t\t\t****************************")
    print("\t\t\t\t\t\tElection Registration System")
    print("\t\t\t\t\t\t****************************")

    print("\n\t\t\t 1) Citizens \n\t\t\t 2) Parties \n\t\t\t 3) Candidates \n\t\t\t 4) exit \n")
    option = input("Enter your option (1 or 2 or 3 or 4) : ")

    return option


def create_citizen_table(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS citizens 
                      (nic VARCHAR(255) PRIMARY KEY, 
                       name VARCHAR(255), 
                       age INT, 
                       state_province VARCHAR(255))''')


def get_citizen_option():
    print("\n\t\t\t\t\t\t____________________________________")
    print("\t\t\t\t\t\tYou are in the Citizens Manage System")
    print("\t\t\t\t\t\t____________________________________")
    print("\n\t\t 1) Add Citizen details \n\t\t 2) Show Citizens details \n\t\t 3) Update Citizens details \n\t\t 4) Delete Citizens details")

    choose = input("Enter Citizen option : ")
    print("\n")
    return choose



def get_citizens_details(cursor):

    cursor.execute("SELECT * FROM citizens")

    citizens = cursor.fetchall()
    return citizens

def show_citizens_details(citizens):

    if not citizens:
        print("No citizen details found.")
    else:
        print("\t\t\t\t\t\t Citizen details:")
        print("\t-----------------------------------------------------------------")
        print("\t: NIC \t\t:\t Name \t\t:\t Age \t\t:\t State/Province :")
        print("\t-----------------------------------------------------------------")

        for citizen in citizens:
            nic, name, age, state_province = citizen
            print(f"\t: {nic} \t\t:\t {name} \t\t:\t  {age} \t\t:\t  {state_province} :")
            print("\t-----------------------------------------------------------------")


def enter_nic():
    nic = input("Enter NIC: ")
    return nic


def check_nic_in_citizens_table(nic, cursor):
    cursor.execute("SELECT COUNT(*) FROM citizens WHERE nic = %s", (nic,))
    count = cursor.fetchone()[0]
    return count > 0


def get_citizen_details():
    name = input("Enter name: ")
    state_province = input("Enter state/province: ")
    age = int(input("Enter age: "))

    return name, state_province, age


class Citizen:
    def __init__(self, nic, name, age, state_province):
        self.nic = nic
        self.name = name
        self.age = age
        self.state_province = state_province

    def __str__(self):
        return f"{self.nic} (NIC: {self.name}, Age: {self.age}, State/Province: {self.state_province})"

    def is_eligible_to_vote(self):
        return self.age > 18


def check_citizen_eligible(citizen, cursor, cnx):
    if citizen.is_eligible_to_vote():
        add_citizen_to_db(citizen, cursor)
        cnx.commit()
        print(f"citizen {citizen.name} added to the database.")
    else:
        print(f"Sorry, {citizen.name} is not eligible to vote.")


def add_citizen_to_db(citizen, cursor):
    sql = '''INSERT INTO citizens (nic, name, age, state_province)
             VALUES (%s, %s, %s, %s)'''
    values = (citizen.nic, citizen.name, citizen.age, citizen.state_province)
    cursor.execute(sql, values)


def get_update_citizen_details(nic, cursor):

    cursor.execute("SELECT * FROM citizens WHERE nic = %s", (nic,))

    citizen_o = cursor.fetchone()
    return citizen_o



def update_citizen_details(citizen_u, cnx, cursor):
    if citizen_u is not None:
        nic_o, name_o, age_o, state_province_o = citizen_u

        print(f"Citizen previous details:")
        print(f"NIC: {nic_o}")
        print(f"Name: {name_o}")
        print(f"Age: {age_o}")
        print(f"State/Province: {state_province_o}")
        print("\n")

        print(f"Enter Citizen current details:")
        new_name = input("Enter name: ")
        new_state_province = input("Enter state/province: ")
        new_age = int(input("Enter age: "))
        citizen = Citizen(nic_o, new_name, new_age, new_state_province)

        sql = '''UPDATE citizens SET name = %s, age = %s, state_province = %s WHERE nic = %s'''
        values = (citizen.name, citizen.age, citizen.state_province, nic_o)
        cursor.execute(sql, values)
        cnx.commit()

        print(f"Citizen details updated successfully.")
    else:
        print("Citizen not found.")


def delete_citizen_details(nic, cursor, cnx):
    count = check_nic_in_citizens_table(nic, cursor)

    if count == 0:
        print("Citizen not registered in the system")
        return

    sql = "DELETE FROM citizens WHERE nic = %s"
    cursor.execute(sql, (nic,))
    cnx.commit()

    sql_delete_candidate = "DELETE FROM candidates WHERE nic = %s"
    cursor.execute(sql_delete_candidate, (nic,))
    cnx.commit()

    print(f"Citizen details deleted successfully.")



def create_party_table(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS parties
                       (name VARCHAR (255) PRIMARY KEY,
                        symbol_name VARCHAR(255))''')


def get_party_option():
    print("\n\t\t\t\t\t\t____________________________________")
    print("\t\t\t\t\t\tYou are in the Parties Manage System")
    print("\t\t\t\t\t\t____________________________________")
    print("\n\t\t 1) Add Party details \n\t\t 2) Show Parties details \n\t\t 3) Update Party details \n\t\t 4) Delete party details\n")

    choose = input("Enter your option : ")
    print("\n")
    return choose


def show_party_details(cursor):
    cursor.execute("SELECT * FROM parties")
    parties = cursor.fetchall()

    if not parties:
        print("No party details found.")
    else:
        print("Party details:")
        for party in parties:
            name, symbol_name = party
            print(f"Name: {name}, Symbol: {symbol_name}")


def input_party_details():
    name = input("Enter name: ")
    symbol_name = input("Enter symbol: ")
    return name, symbol_name


def check_in_party_table(name, symbol_name, cursor):
    cursor.execute("SELECT COUNT(*) FROM parties WHERE name = %s", (name,))
    pn = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM parties WHERE symbol_name = %s", (symbol_name,))
    ps = cursor.fetchone()[0]

    return pn, ps


class Party:
    def __init__(self, name, symbol_name):
        self.name = name
        self.symbol_name = symbol_name


def add_party_to_db(party, cursor):
    sql = '''INSERT INTO parties (name, symbol_name)
                 VALUES (%s, %s)'''
    values = (party.name.lower(), party.symbol_name.lower())
    cursor.execute(sql, values)

    print("Party details added successfully")


def update_party_details(p_name, cursor, cnx):
    cursor.execute("SELECT * FROM parties WHERE name = %s", (p_name,))
    party = cursor.fetchone()

    if party:
        print("Party details:")
        print(f"Name: {party[0]}")
        print(f"Symbol name: {party[1]}")
        print()

        new_name = input("Enter new name: ")
        new_symbol_name = input("Enter new symbol name: ")

        sql = '''UPDATE `parties` SET `name` = %s, `symbol_name` = %s WHERE `name` = %s'''
        values = (new_name, new_symbol_name, p_name)
        cursor.execute(sql, values)
        cnx.commit()

        update_candidates_query = '''UPDATE candidates SET party = %s WHERE party = %s'''
        update_candidates_values = (new_name, p_name)
        cursor.execute(update_candidates_query, update_candidates_values)
        cnx.commit()

        print("Party details updated successfully.")
    else:
        print("Party not found.")


def delete_party_details(party_name, cursor, cnx):
    cursor.execute("DELETE FROM parties WHERE name = %s", (party_name,))
    cnx.commit()
    print(f"Party '{party_name}' details deleted successfully.")

    cursor.execute("DELETE FROM candidates WHERE party = %s", (party_name,))
    cnx.commit()
    print(f"Candidates with party name '{party_name}' deleted successfully.")


def check_party_table(cursor):

    cursor.execute("SELECT COUNT(*) FROM parties")
    party_count = cursor.fetchone()[0]
    return party_count > 0


def get_candidate_option():
    print("\n\t\t\t\t\t\t____________________________________")
    print("\t\t\t\t\t\tYou are in the Candidates Manage System")
    print("\t\t\t\t\t\t____________________________________")
    print(
        "\n\t\t 1) Add Candidate details \n\t\t 2) Show Candidate details \n\t\t 3) Delete Candidate details\n")

    choose = input("Enter your option : ")
    print("\n")
    return choose


def create_candidates_table(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS candidates
                          (nic VARCHAR(255) PRIMARY KEY,
                           party VARCHAR(255),
                           education VARCHAR(255))''')


def get_citizen_by_nic(nic, cursor):
    query = "SELECT * FROM citizens WHERE nic = %s"
    cursor.execute(query, (nic,))
    result = cursor.fetchone()
    nic, name, age, state_province = result
    return nic, name, age, state_province


def input_candidate_details():
    party = input("enter party name: ")
    education = input("enter education qualifications: ")
    return party, education


class Candidate(Citizen):
    def __init__(self, nic, name, age, state_province, party, education):
        super().__init__(nic, name, age, state_province)
        self.party = party
        self.education = education


def add_candidate_to_db(candidate, cursor):
    sql = '''INSERT INTO candidates (nic, party, education)
             VALUES (%s, %s, %s)'''
    values = (candidate.nic, candidate.party, candidate.education)
    cursor.execute(sql, values)


def show_candidates_details(cursor):
    query = '''
            SELECT c.nic, c.name, c.age, c.state_province, ca.party, ca.education
            FROM citizens c
            INNER JOIN candidates ca ON c.nic = ca.nic
        '''
    cursor.execute(query)
    candidates = cursor.fetchall()

    if not candidates:
        print("No candidate details found.")
    else:
        print("\t\t\tCandidate details:")
        print("\t--------------------------------------------------------------------------------------------------------")
        print("\t: NIC \t\t:\t Name \t\t:\t Age \t\t:\t State/Province \t:\t Party \t:\t Education :")
        print("\t--------------------------------------------------------------------------------------------------------")

        for candidate in candidates:
            nic, name, age, state_province, party, education = candidate
            print(f"\t: {nic} \t\t:\t {name} \t\t:\t  {age} \t\t:\t  {state_province} \t:\t  {party} \t\t:\t  {education} :")
            print("\t-------------------------------------------------------------------------------------------------------")




def delete_candidate_details(c_nic, cursor, cnx):

    cursor.execute("DELETE FROM candidates WHERE nic = %s", (c_nic,))
    cnx.commit()
    print(f"Candidates with NIC '{c_nic}' deleted successfully.")





def main():
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
    )
    cursor = cnx.cursor()

    create_database(cursor)

    cnx.database = 'election'

    while True:

        option = home()

        if option == '4':
            break

        if option == '1':

            create_citizen_table(cursor)
            choose = get_citizen_option()

            if choose == '2':

                citizens = get_citizens_details(cursor)
                show_citizens_details(citizens)

            elif choose == '1':
                nic = enter_nic()
                count = check_nic_in_citizens_table(nic, cursor)

                if count == 1:
                    print("User already registered in system")
                    main()

                else:
                    name, state_province, age = get_citizen_details()
                    citizen = Citizen(nic, name, age, state_province)
                    check_citizen_eligible(citizen, cursor, cnx)

            elif choose == '3':

                nic = enter_nic()
                citizen_o = get_update_citizen_details(nic, cursor)
                update_citizen_details(citizen_o, cnx, cursor)

            elif choose == '4':

                nic = enter_nic()
                delete_citizen_details(nic, cursor, cnx)

            else:
                print("\t\tInvalid input")
                main()

        if option == '2':
            create_party_table(cursor)

            choose = get_party_option()

            if choose == '2':
                show_party_details(cursor)

            elif choose == '1':

                name, symbol_name = input_party_details()

                pn, ps = check_in_party_table(name, symbol_name, cursor)

                if pn == 1 and ps == 1:
                    print("This party already registered")
                    home()

                elif ps == 1:
                    print("This party symbol is already exist")
                    home()

                elif pn == 1:
                    print("This party name already exist")
                    home()

                else:
                    party = Party(name, symbol_name)

                    add_party_to_db(party, cursor)

                cnx.commit()

            elif choose == '3':
                p_name = input("Input party name:")
                update_party_details(p_name, cursor, cnx)

            elif choose == '4':
                p_name = input("Input party name:")
                delete_party_details(p_name, cursor, cnx)


        if option == '3':
            create_party_table(cursor)
            choose = get_candidate_option()
            create_candidates_table(cursor)

            if choose == '1':
                party_count = check_party_table(cursor)

                if party_count == 1:
                    nic = enter_nic()
                    count = check_nic_in_citizens_table(nic, cursor)

                    if count == 0:
                        print("Candidate not registered as citizen \n registered as citizen")
                        name, state_province, age = get_citizen_details()
                        citizen = Citizen(nic, name, age, state_province)
                        check_citizen_eligible(citizen, cursor, cnx)

                    else:
                        nic, name, age, state_province = get_citizen_by_nic(nic, cursor)
                        party, education = input_candidate_details()
                        candidate = Candidate(nic, name, age, state_province, party, education)
                        add_candidate_to_db(candidate, cursor)

                        cnx.commit()

            elif choose == '2':

                show_candidates_details(cursor)

            elif choose == '3':
                c_nic = input("Input candidate NIC:")
                delete_candidate_details(c_nic, cursor, cnx)

    cursor.close()
    cnx.close()


if __name__ == "__main__":
    main()
