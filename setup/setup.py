import databaseSetup as db_su
import generateCSV as gen_csv
import fillDatabase as fill_sb

db_su.run()
gen_csv.generateAllCSV()
fill_sb.fill()