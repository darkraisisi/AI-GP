import databaseSetup as db_su
import generateCSV as gen_csv
import fillDatabase as fill_sb

if(input('Are you sure you want to run the setup? y/n') == 'y'):
    db_su.run()
    gen_csv.generateAllCSV()
    fill_sb.fill()