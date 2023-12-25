from rich.table import Table
from rich import print
from rich.panel import Panel
import pyperclip
from getpass import getpass
import utils

panel = Panel("[bold blue]PASSWORD MANAGER[/bold blue]")
print(panel)

utils.initialisedb()

if utils.currentuser() == None:
    username = input("Enter username  : ")
    while True:
        masterpass = getpass("Enter masterpassword :")
        if masterpass ==  getpass("Re-Type :"):
            break
        else:
            print("[yellow]try again[/yellow]")

    authenticate = utils.registeruser(username, masterpass)
    print("[green]user registered  sucessfully[/green]")

else:
    masterpass = getpass("Enter masterpassword : ")
    authenticate = utils.authenticateuser(masterpass)
    print("[green]user logged in sucessfully[/green]")

if authenticate:
    print("""\n [bold]OPTIONS[/bold]:
          1. ADD ENTRY
          2. SHOW/SEARCH ENTRIES
          3. UPDATE ENTRIES 
          4. DELETE ENTRY
          5. RESTORE/EXPORT
          6. EXIT""")
else:
    print("[red]OOPS! something went wrong.[/red]")

while authenticate:
    dbcur = utils.dbwriter()
    op = input("> ")

    if op == "1":
        sitename = input("Enter sitename : ")
        if sitename != "":
            password = input("Enter password (default generate) : ")
            if password == "":
                password = utils.generatepass(10)
            dbcur.execute("INSERT INTO ENTRIES (sitename,password) VALUES (?,?)",(sitename,password))
            print("[green]added new entry[/green]")
        else:
            print("[red]invalid site name[/red]")
            pass

    elif op == "2":
        table = Table(title="VAULT")
        table.add_column("No", justify="left", style="bold")
        table.add_column("site", justify="center")
        table.add_column("password", justify="right")
        dbcur.execute("SELECT no,sitename,password FROM ENTRIES")
        records =  list(dbcur.fetchall())
        for row in records:
            table.add_row(str(row[0]), row[1], row[2])
        print(table)
        try:
            no = int(input("COPY password (0/entryno):"))
            if utils.checkentry(no):
                for i in records:
                    if i[0] == no:
                        pyperclip.copy(i[2])
                        break
                print("[green]sucessfully copied to clipboard[/green]")
            elif no == 0:
                pass
            else:
                print("[red]no entry found[/red]")
        except:
            print("[red]something went wrong[/red]")
            pass


    elif op == "3":
        try:
            no = int(input("Enter the entry no. to update : "))
            if utils.checkentry(no):
                sitename =  input("Enter sitename (default old) : ")
                password = input("Enter password (default old): ")
                if sitename:
                    dbcur.execute("UPDATE ENTRIES SET sitename = ? WHERE no = ?",(sitename,no))
                if password:
                    dbcur.execute("UPDATE ENTRIES SET password = ? WHERE no = ?",(password,no))
                print("[green]updated entry[/green]")
            else:
                print("[red]no entry found[/red]")
        except:
            print("[red]something went wrong[/red]")
            pass

    elif op == "4":
        try:
            no = int(input("Enter entry no. to delete (no / 404 to delete all): "))
            if utils.checkentry(no):
                dbcur.execute("DELETE FROM ENTRIES WHERE no=?",(no,))
                print("[green]deleted entry[/green]")
            elif no == 404:
                dbcur.execute("DELETE FROM ENTRIES")
                print("[green]wiped all the entries[/green]")
            else:
                print("[red]no entry found[/red]")
        except:
            print("[red]something went wrong[/red]")
            pass
    
    elif op == "5":
        dbcur.execute("SELECT * FROM ENTRIES")
        with open("./entries.txt","w") as fp:
            lines = [str(i) + "\n" for i in dbcur.fetchall()]
            fp.writelines(lines)
        print("[green]exported to ./entries.txt[/green]")


    elif op == "6":
        authenticate = False

    else:
        pass


utils.closevault()



