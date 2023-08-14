#! /usr/intel/bin/python 
import os
import time     
import subprocess
import threading
from pathlib import Path

#cmd = 'setenv PYTHON_TEST SUCCESS'
#cmd = 'echo $MR'
#cmd = 'simregress -l $TL/demotion_test/bus_cte/bus_c6demot_lv1.list  -dut bus1_h4c_4M -net -P sc4_normal -Q /core/atom/val/powerv -C "SLES12&&16G" -notify  -trex -save -m passit -ms -vcs +ARGS_IGNORE_UNDEFINED=1  +OVM_VERBOSITY=OVM_MEDIUM  +UVM_VERBOSITY=UVM_MEDIUM -vcs- -ms- -trex- -no_use_ifeed_subdir -no_xs -test_results $TR/python_test'
#os.system(cmd)
#import pipes
#import random
#r = random.randint(1,100)
#print("setenv BLAHBLAH %s" % (pipes.quote(str(r))))


from tkinter import *
from tkinter import ttk
from tkinter import messagebox

simregress_running = False;
def run_simregress(*args):
  global simregress_running;
  simregress_running =True
  trex_input = '';
  vcs_input = '';
  simregress_input ='';
  fuse_input = '';
  simbuild_input = '';
  final_dut_str = '';
  if(dut_drop_str.get() != dut_level0_list[0]):
      simregress_input = simregress_input + " -dut "+dut_drop_str.get() + ' '
      final_dut_str = dut_drop_str.get() 
  else:
    if(len(dut_str.get()) > 0):
      simregress_input = simregress_input + " -dut "+dut_str.get() + ' '
      final_dut_str = dut_str.get() 
  if(len(tmax_str.get()) > 0):
    simregress_input = simregress_input + " -tmax "+ tmax_str.get() + ' '
  if(notify_enable.get()==1) :
    simregress_input += " -notify "
  if(len(result_dir_str.get()) > 0):
    simregress_input = simregress_input + " -test_results "+result_dir_str.get() + ' '
  if(tid_enable.get()==1 and len(tid_str.get())>0):
    simregress_input = simregress_input + " -do_tid "+ tid_str.get() +' '
  
  simregress_input = simregress_input + ' '+ simregress_str.get()+' '
  
  if(len(fuse_str.get()) > 0):
    fuse_input = ' -fuse '+fuse_str.get()+' -fuse- '

  if(dump_fsdb.get() ==1) :
    vcs_input += " +FSDB "
    if(len(fsdb_begin_str.get()) > 0):
      vcs_input = vcs_input + " +FSDB_ON="+fsdb_begin_str.get()+ " "
    if(len(fsdb_end_str.get()) > 0):
      vcs_input = vcs_input + " +FSDB_OFF="+fsdb_end_str.get()+ " " 
  vcs_input = vcs_input + " +OVM_VERBOSITY=OVM_"+verbosity_str.get()+ " UVM_VERBOSITY=UVM_"+verbosity_str.get() 
  vcs_input += ' '
  vcs_input += plusarg_str.get();
  vcs_input += ' '

  if(save_enable.get()==1) :
    trex_input += " -save "

  if(cov_enable.get()==1):
    if(cov_where_str.get() == "both"):
      trex_input += " -casa_args -local -casa_args- "
    if(cov_where_str.get() == "sandbox area only"):
      trex_input += " -casa_args -casa_args- "
    if(cov_where_str.get() == "local result directory only"):
      trex_input += " -casa_args -local_only -casa_args- "
  
  if(skip_run.get()==1) :
    trex_input +=" -m passit "
  else :
    trex_input +=" -m bnlrun "
  trex_input+= ' ' 
  trex_input+= trex_str.get();
  trex_input+= ' '

  cmd = 'simregress -l '+ list_str.get() + ' -net -P sc4_normal -Q '+queue_str.get()+' -C \'SLES12&&'+ memory_str.get()+'\' '+ simregress_input  + ' -trex -ms -vcs +ARGS_IGNORE_UNDEFINED=1 ' + vcs_input  +' -vcs- -ms- '+ trex_input +' -trex- -no_use_ifeed_subdir -no_xs'

  if(simbuild_enable.get()==1):
    if(simbuild_stage_str.get() == "from scratch"):
      cmd = "simbuild -dut "+ final_dut_str +  " && " + cmd
    if(simbuild_stage_str.get() == "from cth_vcs stage"):
      cmd = "simbuild -dut "+ final_dut_str +  " -start cth_vcs  && " +cmd
  
  if(use_head.get()==1):
    if(repo_head_str.get() == "skt"):
      latest_head_str = "$RTLMODELS/skt/cpu/cpu-ertl-skt-head0-latest";
    if(repo_head_str.get() == "sk8"):
      latest_head_str = "$RTLMODELS/skt/cpu/cpu-ertl-sk8-head0-latest";
    if(repo_head_str.get() == "dkt"):
      latest_head_str = "$RTLMODELS/dkt/bus/bus-ertl-dkt-head0-latest";
    
    cmd ="set REPO_REALPATH=`realpath " + latest_head_str + "`;setenv REPO_NAME `basename $REPO_REALPATH`;echo 'repo we are using is';echo $REPO_NAME;setenv REPO_ROOT $REPO_REALPATH ;source /p/hdk/rtl/hdk.rc -cfg atmhdk;setenv REPO_ROOT $REPO_REALPATH;source $REPO_ROOT/cpu/perllib/setup.rc;"  + cmd 
  #os.system(cmd)
  print('\n');
  print("Thread: start")
  print("generated script:\n" + cmd +"\n\nbegin executing!");
  p = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,  bufsize=1, shell=True, executable='/bin/csh')
  run_button['state']='disabled'
  while p.poll() is None: 
    msg = p.stdout.readline().strip() # read a line from the process output
    if msg:
  #    #print(msg)
      text.insert('end', msg+ b"\n" )
      text.see('end')
  run_button['state']='normal';
  print("Thread: end")
  simregress_running=False


recur_running = False;
recur_running_str = '';
def run_scheduler(*args):
  global recur_running
  global recur_running_str
  next_run_delay =0;
  if(recur_str.get() == "daily"):
    next_run_delay = 24; #every 24 hours
  elif(recur_str.get() == "weekly"):
    next_run_delay = 24*7;
  next_run_remaining =0;
  cur_sec = 1;
  while(recur_running):
    if(cur_sec==1):#check at first second of every hour
      cur_sec=60*60;
      if(next_run_remaining == 0):
        print('running recurring regression')
        run_simregress();
        next_run_remaining= next_run_delay
      
      if(next_run_remaining >24 ):
        print("running test " +recur_running_str+" ; next run in "+ str(int(next_run_remaining/24))  +" days and " + str(next_run_remaining%24) + " hour(s)" );
      else:
        print("running test " +recur_running_str+" ; next run in " + str(next_run_remaining) + " hour(s)" );
      next_run_remaining-=1;

    time.sleep(1)
    cur_sec-=1;

def run():
    global recur_running;
    global recur_running_str
    if(recur_str.get()  == 'once'):
      threading.Thread(target=run_simregress, daemon=True).start()
    else:
      if(not recur_running):  
        thread = threading.Thread(target=run_scheduler, daemon=True)
        thread.start()
        recur_running =True;
        recur_running_str = recur_str.get()
      else:
        recur_running = False;
        print("stopped recuring regression")
      change_recur()
    

    #threading.Thread(target=run_simregress).start()
def on_closing():
  global recur_running
  if(recur_running or simregress_running):
    if messagebox.askokcancel("Quit", "There is a test running\nDo you want to quit for sure?"):
      root.destroy()
  else:
    root.destroy()

def test():
    print("Thread: start")

    p = subprocess.Popen("ping -c 4 stackoverflow.com".split(), stdout=subprocess.PIPE,  bufsize=1)
    while p.poll() is None:
        msg = p.stdout.readline().strip() # read a line from the process output
        if msg:
            #print(msg)
            text.insert('end', msg+ b"\n" )

    print("Thread: end")

def hello(*args):
  print('hello')


from tkinter import filedialog

def use_latest_head(*args):
  if(use_head.get() == 1):
    repo_dir_label['state']='disable'
  else:
    repo_dir_label['state']='normal'


def browse_list(*args):
  filename = filedialog.askopenfilename(initialdir = os.getcwd(),
                                          title = "Select a File",
                                          filetypes = (("list files",
                                                        "*.list*"),
                                                        ("trex files",
                                                        "*.trex*"),
                                                       ("all files",
                                                        "*.*")))
  list_str.set(filename);

def choose_dut(*args):
  if(dut_drop_str.get() != dut_level0_list[0] ):
    #dut_str.set(dut_drop_str.get())
    dut_str.set('')
    dut_entry['state']='disabled'
  else:
    dut_str.set('')
    dut_entry['state']='normal'


    

def browse_result_dir(*args):
  filename = filedialog.askdirectory()
  #print(filename)
  result_dir_str.set(filename);

def enabling_tid(*args):
  if tid_enable.get() == 1:
    tid_entry["state"]="normal"
    #tid_label["state"]="normal"
  elif tid_enable.get() ==0:
    tid_entry["state"]="disabled"
    #tid_label["state"]="disabled"


def profile_select(*args):
    profile = profile_str.get();
    if profile == "run regression":
      save_enable.set(1);
      dump_fsdb.set(0);
      cov_enable.set(1);
    elif profile == "reproduce fsdb":
      save_enable.set(0);
      dump_fsdb.set(1);
      cov_enable.set(0);
    enabling_coverage();
    enabling_fsdb_dump();
def enabling_simbuild():
  if simbuild_enable.get()==0 :    
    simbuild_stage_drop['state']="disabled";
  else:
    simbuild_stage_drop['state']="normal";

def enabling_fsdb_dump():
  if dump_fsdb.get() == 1:
    fsdb_begin_label["state"]="normal"
    fsdb_begin["state"]="normal"
    fsdb_end_label["state"]="normal"
    fsdb_end["state"]="normal"
  else:
    fsdb_begin_label["state"]="disabled"
    fsdb_begin["state"]="disabled"
    fsdb_end_label["state"]="disabled"
    fsdb_end["state"]="disabled"

def enabling_coverage():
  if cov_enable.get() == 1:
    #cov_local_button["state"] = "normal"
    #cov_local.set(1) ;
    #cov_sandbox_button["state"] = "normal"
    #cov_sandbox.set(1) ;
    cov_where_drop["state"] = "normal"
    cov_where_label["state"] = "normal"

  else:
    #cov_local_button["state"] = "disabled"
    #cov_local.set(0) ;
    #cov_sandbox_button["state"] = "disabled"
    #cov_sandbox.set(0) ;
    cov_where_drop["state"] = "disabled"
    cov_where_label["state"] = "disabled"

 

def disabling_coverage():
  if cov_local.get() == 0 and cov_sandbox.get() == 0:
    cov_enable.set(0);
    cov_local_button["state"] = "disabled"
    cov_sandbox_button["state"] = "disabled"

def change_recur(*args):
  global recur_running
  if recur_str.get() != "once" and recur_running  :
    run_button.config(text="STOP")
  else:
    run_button.config(text="RUN")

root = Tk()
root.resizable(False,False)

#root.geometry("600x700")
#root.grid_propagate(0)
#root.pack_propagate(0)
repo_root = os.getenv('REPO_ROOT');
model_name = ''
if(repo_root is not None) :
  model_name=os.path.basename(repo_root)
  root.title("EZsimregress ("+model_name+')' )
else:
  root.title("EZsimregress" )

repo_head_str = StringVar();
repo_head_str.set("dkt");
repo_head_options = ["", "dkt", "sk8","skt"];

simbuild_stage_str = StringVar()
simbuild_stage_str.set("from scratch");
simbuild_stage_options = ["", "from scratch", "from cth_vcs stage"];

use_head=IntVar()
tid_enable=IntVar()
save_enable = IntVar()

cov_enable = IntVar()
cov_local = IntVar()
cov_sandbox = IntVar()
cov_where_str =StringVar();
cov_where_options = ["","local result dir only", "sandbox area only","both"];

verbosity_str =StringVar();
verbosity_options = ["","LOW", "MEDIUM","HIGH","FULL","DEBUG" ];

profile_str =StringVar();
profile_options = ["choose an options","run regression", "reproduce fsdb"];

recur_str =StringVar();
recur_options = ["","once", "daily", "weekly"];

dump_fsdb = IntVar()
notify_enable = IntVar()

mainframe = ttk.Frame(root, padding=3)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

basic_frame = ttk.Frame(mainframe,borderwidth=2,relief=RAISED,padding=3);
basic_frame.grid(column=0, row=0, stick='we');


cur_row=0;
repo_frame = ttk.Frame(basic_frame)
repo_frame.grid(row=cur_row, sticky=W)

ttk.Label(repo_frame, text="$REPO_ROOT: ").pack(side=LEFT)
repo_dir_frame = ttk.Frame(repo_frame,borderwidth=1,relief=RIDGE,padding=2 )
repo_dir_frame.pack(side=LEFT)
repo_display = '';
if repo_root is None:
  repo_display = " not yet specified, either select the latest repo below or close this window"
elif len(repo_root)>75:
  begin_index=len(repo_root)-75
  repo_display = repo_root[begin_index:]
  repo_display = "..." + repo_display + "  "
repo_dir_label = ttk.Label(repo_dir_frame, text=repo_display)
repo_dir_label.pack(side=LEFT)

cur_row+=1;

repo_head_frame = ttk.Frame(basic_frame,padding='0 2 0 0')
repo_head_frame.grid(row=cur_row,sticky='w')
repo_head_button = ttk.Checkbutton(repo_head_frame, text='use',variable=use_head, onvalue=1, offvalue=0, command=use_latest_head)
repo_head_button.pack(side=LEFT,padx='92 0'); 
repo_head_drop = ttk.OptionMenu(repo_head_frame, repo_head_str, *repo_head_options )
repo_head_drop.pack(side=LEFT);
ttk.Label(repo_head_frame,text="head0 latest release instead").pack(side=LEFT)
cur_row+=1

perlscript = """
use strict;
use vars qw(%TaskConfig);

chdir "$ENV{'RTLMODELS'}/dkt/bus/bus-ertl-dkt-head0-latest";
my $c ="bus";
my $s ="dkt-head0";
my $e ="default";
require "$ENV{'RTLMODELS'}/dkt/bus/bus-ertl-dkt-head0-latest/config/TaskConfig.common.pm";
require "$ENV{'RTLMODELS'}/dkt/bus/bus-ertl-dkt-head0-latest/config/TaskConfig.hdk.${s}.${c}.pl";
my @duts = @{$TaskConfig{'duts'}{$c}{$s}};
my @stages = @{$TaskConfig{'stages'}};
foreach my $dut (@duts) {
	foreach my $stage (@stages) {
	if (defined $TaskConfig{$c}{$s}{$dut}{$stage}{$e} and $stage eq 'level0') {
		print "$dut ";
	}
  }
}
print "\n";
"""
dut_level0_list = subprocess.check_output(['perl', '-e', perlscript], shell=False).decode().split()
dut_level0_list.insert(0, 'select below');

dut_frame = ttk.Frame(basic_frame,padding= '0 5 5 0')
dut_frame.grid(row=cur_row, sticky=W)
ttk.Label(dut_frame, text="dut:").pack(side=LEFT)

dut_drop_str = StringVar()
dut_drop = ttk.OptionMenu(dut_frame, dut_drop_str,dut_level0_list[0], *dut_level0_list, command = choose_dut)
dut_drop.config(width=20)
dut_drop.pack(side=LEFT,padx="2 0")

ttk.Label(dut_frame, text="  or specify here: ").pack(side=LEFT, )

dut_str = StringVar()
dut_entry = ttk.Entry(dut_frame, width=25, textvariable=dut_str)
dut_entry.pack(side=LEFT)




cur_row+=1

list_frame = ttk.Frame(basic_frame)
list_frame.grid(row=cur_row, sticky=W)
ttk.Label(list_frame, text="list: ").pack(side=LEFT)
list_str = StringVar()
browse_list_button = ttk.Button(list_frame, text='browse',command=browse_list)
browse_list_button.pack(side=LEFT)
list_entry = ttk.Entry(list_frame, width=70, textvariable=list_str)
list_entry.pack(side=LEFT)
cur_row+=1


tid_frame = ttk.Frame(basic_frame)
tid_frame.grid(row=cur_row, sticky=W)
tid_button = ttk.Checkbutton(tid_frame, text='only run selected tests with tid:',variable=tid_enable, onvalue=1, offvalue=0, command =enabling_tid)
tid_button.pack(side=LEFT);
#tid_label= ttk.Label(tid_frame, text="TID lists:")
#tid_label.pack(side=LEFT)
tid_str = StringVar()
tid_entry = ttk.Entry(tid_frame, width=56, textvariable=tid_str)
tid_entry.pack(side=LEFT)
#tid_label["state"]="disabled"
tid_entry["state"]="disabled"
cur_row+=1



result_dir_frame = ttk.Frame(basic_frame)
result_dir_frame.grid(row=cur_row, sticky=W)
ttk.Label(result_dir_frame, text="result directory: ").pack(side=LEFT)
browse_result_dir_button = ttk.Button(result_dir_frame, text='browse',command=browse_result_dir)
browse_result_dir_button.pack(side=LEFT)

result_dir_str = StringVar()
result_dir_entry = ttk.Entry(result_dir_frame,width=60, textvariable=result_dir_str)
result_dir_entry.pack(side=LEFT)
cur_row+=1

setting_wrapper_frame = ttk.Frame(mainframe);
setting_wrapper_frame.grid(row=1, stick='we');
setting_wrapper_frame.grid_columnconfigure(0, weight=12)
setting_wrapper_frame.grid_columnconfigure(1, weight=10)

setting_frame = ttk.Frame(setting_wrapper_frame,borderwidth=2,relief=RAISED,padding=3);
setting_frame.grid(column=0, row=0, stick='we');
cur_row=0;

profile_frame = ttk.Frame(setting_frame)
profile_frame.grid(row=cur_row, sticky=W)
profile_label = ttk.Label(profile_frame, text="I want to...")
profile_label.pack(side=LEFT)
profile_str.set("reproduce fsdb");
profile_drop = ttk.OptionMenu(profile_frame, profile_str, *profile_options, command=profile_select )
profile_drop.pack(side=LEFT);
cur_row+=1

simbuild_enable=IntVar()
simbuild_frame = ttk.Frame(setting_frame)
simbuild_frame.grid(row=cur_row, sticky=W)
simbuild_button = ttk.Checkbutton(simbuild_frame, text='build the dut first ',variable=simbuild_enable, onvalue=1, offvalue=0, command=enabling_simbuild)
simbuild_button.pack(side=LEFT) 
simbuild_stage_drop = ttk.OptionMenu( simbuild_frame, simbuild_stage_str, *simbuild_stage_options )
simbuild_stage_drop.pack(side=LEFT)
simbuild_stage_drop['state']="disabled";
cur_row+=1


dump_fsdb_frame = ttk.Frame(setting_frame)
dump_fsdb_frame.grid(row=cur_row, sticky=W)
dump_fsdb_button = ttk.Checkbutton(dump_fsdb_frame, text='dump FSDB',variable=dump_fsdb, onvalue=1, offvalue=0, command=enabling_fsdb_dump)
dump_fsdb_button.pack(side=LEFT) 

fsdb_begin_label = ttk.Label(dump_fsdb_frame, text="begin ")
fsdb_begin_label.pack(side=LEFT)
fsdb_begin_str = StringVar()
fsdb_begin = ttk.Entry(dump_fsdb_frame, width=6, textvariable=fsdb_begin_str)
fsdb_begin.pack(side=LEFT)
fsdb_begin_label["state"]="disabled"
fsdb_begin["state"]="disabled"

fsdb_end_label = ttk.Label(dump_fsdb_frame, text="end ")
fsdb_end_label.pack(side=LEFT)
fsdb_end_str = StringVar()
fsdb_end = ttk.Entry(dump_fsdb_frame, width=6, textvariable=fsdb_end_str)
fsdb_end.pack(side=LEFT)
fsdb_end_label["state"]="disabled"
fsdb_end["state"]="disabled"
cur_row+=1

save_button = ttk.Checkbutton(setting_frame, text='only save failing test result',variable=save_enable, onvalue=1, offvalue=0)
save_button.grid( row=cur_row,sticky=W); 
cur_row+=1


cov_frame =ttk.Frame(setting_frame)
cov_frame.grid(row=cur_row, sticky=W)
cov_button = ttk.Checkbutton(cov_frame, text='enable coverage',variable=cov_enable, onvalue=1, offvalue=0, command=enabling_coverage)
cov_button.grid( row=0,column=0,sticky=W); 
cov_where_label = ttk.Label(cov_frame, text="save coverage result to")
cov_where_label.grid(column=0, row=1, sticky=W)
cov_where_str.set("sandbox area only");
cov_where_drop = ttk.OptionMenu( cov_frame, cov_where_str, *cov_where_options )
cov_where_drop.grid(column=1, row=1,sticky=W);
cov_where_drop["state"] = "disabled"
cov_where_label["state"] = "disabled"
cur_row+=1

verbosity_frame=ttk.Frame(setting_frame)
verbosity_frame.grid(row=cur_row, sticky=W)
verbosity_label = ttk.Label(verbosity_frame, text="verbosity:")
verbosity_label.pack(side=LEFT)
verbosity_str.set("MEDIUM");
verbosity_drop = ttk.OptionMenu( verbosity_frame, verbosity_str, *verbosity_options )
verbosity_drop.pack(side=LEFT)
cur_row+=1
#cov_local_button = ttk.Checkbutton(setting_frame, text='save coverage vdb locally toAresult directory',variable=cov_local, onvalue=1, offvalue=0, command=disabling_coverage)
#cov_local_button.grid( row=cur_row); 
#cov_local_button["state"] = "disabled"
#cur_row+=1

#cov_sandbox_button = ttk.Checkbutton(setting_frame, text='send coverage vdb to sandbox',variable=cov_sandbox, onvalue=1, offvalue=0, command=disabling_coverage)
#cov_sandbox_button.grid( row=cur_row);
#cov_sandbox_button["state"] = "disabled"
#cur_row+=1


skip_run = IntVar();
skip_run.set(0)
skip_run_button = ttk.Checkbutton(setting_frame, text='skip bnlrun phrase',variable=skip_run, onvalue=1, offvalue=0)
skip_run_button.grid( row=cur_row, sticky=W);


cur_row+=1


notify_enable.set(1);
notify_button = ttk.Checkbutton(setting_frame, text='email me when done',variable=notify_enable, onvalue=1, offvalue=0)
notify_button.grid( row=cur_row, sticky=W); 
cur_row+=1

arg_width  = 75
arg_frame = ttk.Frame(mainframe,borderwidth=2,relief=RAISED,padding=3)
arg_frame.grid(row=2,sticky="ew") 

ttk.Label(arg_frame, text="Additional Arguments ").grid(row=0,columnspan=2)


ttk.Label(arg_frame, text="plusarg: ").grid(row=1,column=0,sticky=W)
plusarg_str = StringVar()
plusarg_entry = ttk.Entry(arg_frame, width=arg_width, textvariable=plusarg_str)
plusarg_entry.grid(row=1,column=1,sticky='ew')

ttk.Label(arg_frame, text="fuse: ").grid(row=2,column=0,sticky=W)
fuse_str = StringVar()
fuse_entry = ttk.Entry(arg_frame, width=arg_width, textvariable=fuse_str)
fuse_entry.grid(row=2,column=1,sticky=W)

ttk.Label(arg_frame, text="trex: ").grid(row=3,column=0,sticky=W)
trex_str = StringVar()
trex_entry = ttk.Entry(arg_frame, width=arg_width, textvariable=trex_str)
trex_entry.grid(row=3,column=1,sticky=W)

ttk.Label(arg_frame, text="simregress: ").grid(row=4,column=0,sticky=W)
simregress_str = StringVar()
simregress_entry = ttk.Entry(arg_frame, width=arg_width, textvariable=simregress_str)
simregress_entry.grid(row=4,column=1,sticky=W)

setting2_row =0 
setting2_frame = ttk.Frame(setting_wrapper_frame,borderwidth=2,relief=RAISED,padding=3);
setting2_frame.grid(column=1, row=0, sticky='wesn');
ttk.Label(setting2_frame, text="netbatch setting:").grid(column=0,row=0, sticky='we',pady=2);

queue_frame = ttk.Frame(setting2_frame)
queue_frame.grid(row=1, sticky='we')
ttk.Label(queue_frame, text="queue: ").pack(side=LEFT)
queue_str = StringVar()
queue_str.set("/core/atom/val/powerv")
queue_entry = ttk.Entry(queue_frame, width=20, textvariable=queue_str)
queue_entry.pack(side=LEFT)

memory_frame = ttk.Frame(setting2_frame)
memory_frame.grid(row=2, sticky=W)
ttk.Label(memory_frame, text="memory: ").pack(side=LEFT)
memory_str = StringVar()
memory_str.set("16G")
memory_entry = ttk.Entry(memory_frame, width=4, textvariable=memory_str)
memory_entry.pack(side=LEFT)

tmax_frame = ttk.Frame(setting2_frame)
tmax_frame.grid(row=3, sticky=W)
ttk.Label(tmax_frame, text="max total jobs: ").pack(side=LEFT)
tmax_str = StringVar()
tmax_str.set("1000")
tmax_entry = ttk.Entry(tmax_frame, width=5, textvariable=tmax_str)
tmax_entry.pack(side=LEFT)


run_button = ttk.Button(mainframe, text='RUN',command=run)
#run_button = ttk.Button(mainframe, text='RUN',command=run)
run_button.grid( row=3); 

recur_frame=ttk.Frame(mainframe)
recur_frame.grid(row=3, column=0, sticky=W)
recur_label = ttk.Label(recur_frame, text="run")
recur_label.pack(side=LEFT)
recur_str.set("once");
recur_drop = ttk.OptionMenu( recur_frame, recur_str, *recur_options, command=change_recur )
recur_drop.pack(side=LEFT)

class RedirectText(object):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, text_ctrl):
        """Constructor"""
        self.widget = text_ctrl
        
    #----------------------------------------------------------------------
    def write(self, string):
        """"""
        self.widget.insert('end', string)
        self.widget.see('end')


text = Text(mainframe,width=85)
text.grid(row=4,column=0);
#text_error = Text(mainframe,width=80)
#text_error.grid(row=5,column=0);
#scrollbar = ttk.Scrollbar(text, orient=VERTICAL)
#scrollbar.grid()

old_stdout = sys.stdout    
sys.stdout = RedirectText(text)


profile_select();

#root.bind("<Return>", run_simregress)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

#print('ezsimregress done')
sys.stdout = old_stdout



