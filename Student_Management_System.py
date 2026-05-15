import pandas as pd
import os 
SUBJECTS = ["PHYSICS","CHEMISTRY","MATHS","ENGLISH","COMPUTER","HINDI"]


def get_valid_marks(subject):
    while True:
        try:    
            sub_marks = int(input(f"\t..Enter the {subject} marks:"))
            if 0 <= sub_marks <= 100:
                return sub_marks
            else:
                print("Enter a valid marks i.e. btw 0 to 100")
        except ValueError:
            print("Invalid input!")
#-------------------------------------------------------CHECKS MARKS--------------------------------------------------------------------


#-------------------------------------------------------CREATE FILE--------------------------------------------------------------------
def create_file():#takes file name as input and used to create a newfile haveing the name as taken
    """Create a CSV file with coloumns inside it"""
    filename = input("\t..Enter the Filename(or 0 to go back):") + '.csv'
    
    if filename == "0.csv":
        return
    
    pd.DataFrame(columns=["Name","Roll_No","Gender","PHYSICS","CHEMISTRY","MATHS","ENGLISH","COMPUTER","HINDI"]).to_csv(filename,index=False) 
    print(f"\nNew file {filename} created successfully!\n")

#-------------------------------------------------------DISPLAY FILE--------------------------------------------------------------------
def display_file(filename):#prints the data inside the file into a dataferame
    """Display the data inside the file into a DataFrame """
    print("\n")
    d_file = pd.read_csv(filename,encoding = "utf-8")
    if d_file.empty:
        print("No record found or file is empty!")
        return
    else:
        print(d_file)
    print('\n')
#-------------------------------------------------------ADD STUDENT--------------------------------------------------------------------

def add_student(filename):

    """Adds a new student's record to the given CSV file."""
    while True:
        try:
            df = pd.read_csv(filename,encoding = "utf-8")
            
            std_roll = input("\t..Enter student roll(or 0 to go back):")
            if std_roll == "0":
                return
            
            result = df[df["Roll_No"].astype(str) == std_roll]
            if result.empty:
                
                std_name = input("\t..Enter student name:").title()
                while True:
                    std_gender = input('\t..Enter student gender(M/F):').upper()
                    if std_gender in ["F","M"]:
                        break
                    print("\nInvalid Gender!\n")
                        
                phy_marks = get_valid_marks("PHYSICS")
                chem_marks = get_valid_marks("CHEMISTRY")
                maths_marks = get_valid_marks("MATHS")
                eng_marks = get_valid_marks("ENGLISH")
                comp_marks = get_valid_marks("COMPUTER")
                hindi_marks = get_valid_marks("HINDI")
                print("\n")
                    
                add_std = {"Name":std_name,"Roll_No":std_roll,"Gender":std_gender,"PHYSICS":phy_marks,
                           "CHEMISTRY":chem_marks,"MATHS":maths_marks,"ENGLISH":eng_marks,"COMPUTER":comp_marks,
                         "HINDI":hindi_marks}
    
                df.loc[len(df)] = add_std
                df.to_csv(filename,index = False)
                print(f'\t..{std_name} added successfully! to {filename}\n')
                op = input("\t..Continue Adding Student(Y/N):").upper()
                if op == 'Y':
                    continue
                elif op == 'N':
                    break
                else:
                    print("Invalid Input!")
                    break
            else:
                print(f"\t\n..Roll Number {std_roll} is already added")
                print(result.to_string(index = False,justify = "center"))
                
                op = input("\t..Continue Adding Student? (Y/N or to quit 'Q'):").upper()
                if op in ["Q","N"]:
                    break
                else:
                    print("..Invalid Input!\n")
                print("\n")

        except FileNotFoundError:
            print("\nFile not found! Please create or specify the correct file name!.\n")
            return
       
    
#-------------------------------------------------------SEARCH STUDENT--------------------------------------------------------------------
def search_std(filename):
    """Search student based on their Name or Roll_No."""

    try:
        df = pd.read_csv(filename)

        if df.empty:
            print('\n! The File is empty - no record found!\n')
            return
        print("\n")
        print('\tSearch Student by:')
        print('\t..1.Name')
        print('\t..2.Roll_No\n')

        choice = int(input("\t..Enter your choice(1/2 or 0 to go back): "))
            
        if choice == 0:
            return
        elif choice == 1:
            name = input("\t..Enter the Name of the student: ").strip().lower()
            result = df[df["Name"].str.lower() == name]

        elif choice == 2:
            roll = input("\t..Enter the Roll_No of the student: ").strip()  
            result = df[df["Roll_No"].astype(str) == roll]           
        else:
            print('\n Invalid choice!\n')
                
        if not result.empty:
            print("\nStudent Record found!\n:")
            print('\n')
            print(result.to_string(index = False,justify = "center"))
            print("\n")

        else:
            print("\t..NO matching record found.\n")
    except ValueError:
        print("Invalid option choosen!")
    except FileNotFoundError:
        print("\n file not found! Please create or specify the correct file name!.\n")

#-------------------------------------------------------UPDATE STUDENT RECORD--------------------------------------------------------------------

def update_student_marks(filename):
    try:
        df = pd.read_csv(filename)

        if df.empty:
            print('File is Empty! Please create or specify correct name of the file.')

        roll = input("\t..Enter the Roll number of the student to update marks(or 0 to go back):").strip()
        if roll == "0":
            return
        
        result = df[df["Roll_No"].astype(str) == roll]
        
        if result.empty:
            print(f"\nNo! Student found with Roll Number {roll}.")
            print("Please! Add a Student to Update their Marks!")
            return 
        #Display the current Record
        print("\nCurrent Record:\n")
        print(result.to_string(index=False,justify="center"))
        
        #This Loop will keep asking for the marks untill it inpuut is provided
        while True:
        #Ask Which subject(s) to update
           print("Choose the below subject to update the marks:\n")
           print("1.PHYSICS\n2.CHEMISTRY\n3.MATHS\n4.ENGLISH\n5.COMPUTER\n6.HINDI\n7.EXIT")
           try:   
               sub = int(input("Choose SUBJECT by Serial Number: "))
           except ValueError:
               print("Invalid option choosen!")
               continue
           if sub == 7:
                break

           elif sub < 1 or sub > 7:
               print("Invalid subject name! Try Again.")
               continue
            
           subject_name = SUBJECTS[sub-1] 
           new_marks = get_valid_marks(subject_name)
          
           df.loc[df["Roll_No"].astype(str) == roll,subject_name] = new_marks
           print(f"\nUpdated {subject_name} marks successfully!\n")

        # save changes
        df.to_csv(filename,index=False)
        
        updated_record = df[df["Roll_No"].astype(str)== roll ]
        
        print(f"Student record for Roll Number {roll} updated successfully!")
        print('\nUpdated Record:\n')
        print(updated_record.to_string(index=False,justify="center"))

    except FileNotFoundError:
        print("\nFile Not Found! Please create or specify the correct file name.")



#-------------------------------------------------------DELETE STUDENT RECORD--------------------------------------------------------------------

def delete_std(filename):
    "Takes std Roll_No and delete that particular student."
    try:
        df = pd.read_csv(filename)
        
        if df.empty:
            print(f"File {filename} is empty.Please create or specify the correct name of the file.")
            return 
        
        roll = input("Entert the student Roll_No to delete:")
        
        
        if not roll:
            print("Roll Number cann't be empty!")
            return
        
        match = df[df['Roll_No'].astype(str)==roll]

        if  match.empty:
            print(f"\nNo! Student found with Roll Number {roll}.")
            print("\nPlease,First add a student to delete it.\n")
            return
           
        print(f'Student with Roll Number {roll} is present in the record!\n')
        print(match.to_string(index=False,justify="center"))

        final_choice = input(f'Delete {roll} from the record(Y/N):').upper()

        if  final_choice != "Y":
            print(f'{roll} is not deleted.Returning back to Main Menu!\n')
            print()
            return
            
        df.drop(match.index,axis=0,inplace= True)
        df.to_csv(filename,index=False)
        print(f"Student record of Roll_No.{roll} is deleted Successfully!\n")
             
    except ValueError:
        print("Invalid option choosen!")
    except FileNotFoundError:
        print("\nFile Not Found! Please create or specify the correct file name.\n")

    



            


















#-------------------------------------------------------MAIN FUNCTION--------------------------------------------------------------------
 
def main():
    print("\n---------------Welcome to Student Management System!---------------\n")
    while True:
        print('1.To Create file for a Grade(Ex: Grade10A.csv , Note: Use only CSV file.)')
        print('2.To Display the Data inside the file.')
        print("3.To Add a student.")
        print("4.To Search Student By Name or Roll_No.")
        print("5.To Update marks of the students.")
        print("6.To Delete a Student Record.")
        print('7.To EXIT!')
        
        try:
            choice = int(input("\nEnter the number as per the opitons to choose:->"))
        
            if choice == 1:
                create_file()
    
            elif choice == 2:
                print("\n")
                filename = input("\t..Enter the Filename(or 0 to go back):") + '.csv'
                if  filename == "0.csv":
                    continue
                if not os.path.exists(filename):
                    print(f"File {filename} not found. Please create it first.")
                    continue
                display_file(filename)
                
            elif choice == 3:
                print("\n")
                filename = input("\t..Enter the FileName:")  + ".csv"
                if not os.path.exists(filename):
                    print(f"File {filename} not found. Please create it first.")
                else:
                    add_student(filename)
                
            elif choice == 4:
                print("\n")
                filename = input("\t..Enter the FileName:") + ".csv"
                if not os.path.exists(filename):
                    print(f"File {filename} not found. Please create it first.")
                else:
                    search_std(filename)
    
            elif choice == 5:
                print("\n")
                filename = input("\t..Enter the FileName:") + ".csv"
                update_student_marks(filename)
            
            elif choice == 6:
                print("\n")
                filename = input("\t..Enter the FileName:") + ".csv"
                delete_std(filename)
    
            elif choice == 7:
                print("\n..Thank You! Please Visit Again!\n")
                break
            else:
                print("\nOption doesn't exist!")
                print()
        except ValueError:
            print("Invalid option choosen!")
            continue

if __name__ == "__main__":
    main()



            
            
            
77