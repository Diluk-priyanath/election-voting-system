import mysql.connector
import matplotlib.pyplot as plt

def print_section_header(section_name):
    line = "=" * 50
    header = f"{section_name.upper()}"
    print(f"\n{line}\n\t{header}\n{line}\n")

def print_centered(message):
    padding = " " * ((40 - len(message)) // 2)
    print(f"{padding}{message}")

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="election"
)

# Create a cursor to execute SQL queries
cursor = db.cursor()

# Create the 'votes' table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS votes (
    party VARCHAR(255) NOT NULL,
    vote_count INT DEFAULT 0,
    PRIMARY KEY (party)
)
"""
cursor.execute(create_table_query)
db.commit()

# Create the 'voters' table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS voters (
    nic VARCHAR(255) NOT NULL,
    PRIMARY KEY (nic)
)
"""
cursor.execute(create_table_query)
db.commit()

# Display the Election Voting System header
print("\n")
print("\t\t\t\t&&&&&&&&&&&&&&&&&&&&&&")
print("\t\t\t\tELECTION VOTING SYSTEM")
print("\t\t\t\t&&&&&&&&&&&&&&&&&&&&&&")
print("\n")

# Allow citizens to vote for candidates
while True:
    print_section_header("\tENTER YOUR DETAILS")
    citizen_nic = input("\tEnter citizen's NIC (or 'q' to quit): ")
    if citizen_nic == "q":
        break

    # Check if the citizen has already voted
    query = "SELECT nic FROM voters WHERE nic = %s"
    cursor.execute(query, (citizen_nic,))
    result = cursor.fetchone()

    if result:
        print_centered("\tYou have already voted. You cannot vote again.")
        continue

    # Retrieve the citizen's state_province
    query = "SELECT state_province FROM citizens WHERE nic = %s"
    cursor.execute(query, (citizen_nic,))
    result = cursor.fetchone()

    if result:
        state_province = result[0]

        # Retrieve the eligible candidates for the citizen's state_province
        query = """
            SELECT candidates.nic, parties.name
            FROM candidates
            INNER JOIN parties ON candidates.party = parties.name
            WHERE candidates.nic IN (
                SELECT nic
                FROM citizens
                WHERE state_province = %s
            )
        """
        cursor.execute(query, (state_province,))
        results = cursor.fetchall()

        if results:
            print_section_header("\tAVAILABLE CANDIDATES")
            # Display the available candidates to citizens
            for row in results:
                candidate_nic = row[0]
                party_name = row[1]
                print_centered(f"\t{candidate_nic} ({party_name})")

            # Allow citizens to vote up to 3 candidates
            votes_count = 0
            print_section_header("\tVOTE SELECTION")
            while votes_count < 3:
                candidate_nic = input("\tEnter candidate's NIC (or 's' to skip): ")
                if candidate_nic == "s":
                    break

                # Check if the candidate is eligible for the citizen's state_province
                query = """
                    SELECT candidates.nic
                    FROM candidates
                    INNER JOIN parties ON candidates.party = parties.name
                    WHERE candidates.nic = %s AND candidates.nic IN (
                        SELECT nic
                        FROM citizens
                        WHERE state_province = %s
                    )
                """
                cursor.execute(query, (candidate_nic, state_province))
                result = cursor.fetchone()

                if result:
                    # Retrieve the party name for the selected candidate
                    party_name_query = "SELECT party FROM candidates WHERE nic = %s"
                    cursor.execute(party_name_query, (candidate_nic,))
                    party_name = cursor.fetchone()[0]

                    # Record the vote in the database
                    query = "INSERT INTO votes (party, vote_count) VALUES (%s, 1) ON DUPLICATE KEY UPDATE vote_count = vote_count + 1"
                    cursor.execute(query, (party_name,))
                    db.commit()
                    print_centered("\tVote recorded successfully!")
                    votes_count += 1
                else:
                    print_centered("\tInvalid candidate. Please try again.")

            if votes_count == 0:
                print_centered("\tYou have not used any votes.")

            # Add the citizen's NIC to the 'voters' table
            query = "INSERT INTO voters (nic) VALUES (%s)"
            cursor.execute(query, (citizen_nic,))
            db.commit()
        else:
            print_centered("\tNo eligible candidates for your state_province.")
    else:
        print_centered("\tInvalid citizen. Please try again.")

print_section_header("\tVOTE RESULTS")
# Retrieve the votes for each party
query = "SELECT party, SUM(vote_count) as total_votes FROM votes GROUP BY party"
cursor.execute(query)
results = cursor.fetchall()

# Separate party names and vote counts into two lists
party_names = [row[0] for row in results]
vote_counts = [row[1] for row in results]

# Plot the graph
plt.bar(party_names, vote_counts)
plt.xlabel("Parties")
plt.ylabel("Vote Counts")
plt.title("Votes by Party")
plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
plt.show()

# Close the database connection
db.close()
