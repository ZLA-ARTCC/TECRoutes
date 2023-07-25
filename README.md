# TECRoutes
Epic TEC route magic

These files enclosed are used to create TEC routes in a format for our Alias file. Here are the instructions on how to use it:

1) After every AIRAC cycle update, download prefroutes_db.csv from the FAA website and place in the same directory. 
2) Run generateapts.py using the command py generateapts.py. This will generate a list of TEC route airports in ZLA.
3) Run optimizedtecmagic.py  using the command py optimizedtecmagic.py. This will generate a file named tecoutput.tec and tcompare.csv. Using a text editor, the contents of tecoutput.tec can be copy/pasted into the Alias file.
4) Run  teccompare.py. Place the previous AIRAC cycle's version of tecroutecompare.csv into the same directory. Follow the instructions given by the program. This will generate a list of changes/new routes/updates in the file named changefile.tec.

Enjoy! 
