from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter import font
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from IPython import InteractiveShell
from matplotlib.ticker import MaxNLocator
from wordcloud import WordCloud, STOPWORDS
from nltk import *


# ---------------------------------------------------------------------------------------------------------------------------------------
# Improving the data ##1
### Adding one more column of "Day" for better analysis, here we use datetime library which help us to do this task easily.
weeks = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
}




# How many outputs do you want to display for each block?
InteractiveShell.ast_node_interactivity = "all"

# How many output summary rows do you want to display?
pd.set_option('display.max_rows', None)

# How many output summary columns do you want to display?
pd.set_option('display.max_columns', None)




def reloadData():
    global data
    clearOutput()


def generateOutputData():
    global output
    output.clear()
    # Basic statistics
    # Extracting basic statistics from the dataset :
    output.append("Extracting basic statistics from the dataset ")
    total_messages = data.shape[0]
    media_messages = data[data['text_message'] == '<Media omitted>'].shape[0]
    links = np.sum(data.urlcount)
    output.append('Group Chatting Status : ')
    output.append('Total Number of Messages : {}'.format(total_messages))
    output.append('Total Number of Media Messages : {}'.format(media_messages))
    output.append('Total Number of Links : {}'.format(links))

    # print the total no. of messages sent by each user :
    ### Creates a list of unique Authors
    output.append("")
    output.append("TOTAL NUMBER OF MESSAGES SENT BY EACH USER")
    l = data.sender.unique()
    for i in range(len(l)):
        ### Filtering out messages of particular user
        req_df = data[data["sender"] == l[i]]
        ### req_df will contain messages of only one particular user
        output.append(str(l[i]) + '  ->  ' + str(req_df.shape[0]))
    output.append("")

    # print total messages sent on each day of the week :
    output.append("TOTAL MESSAGES SENT ON EACH DAY OF THE WEEK")
    l = data.Day.unique()
    for i in range(len(l)):
        ### Filtering out messages of particular user
        req_df = data[data["Day"] == l[i]]
        ### req_df will contain messages of only one particular user
        output.append(str(l[i]) + '  ->  ' + str(req_df.shape[0]))
    output.append("")



def cleanData():
    global data
    # Extract datetime
    data[['datetime_str', 'text_2']] = data["text"].str.split(" - ", 1, expand=True)
    data["datetime"] = pd.to_datetime(data["datetime_str"], format="%d/%m/%Y, %I:%M %p", errors='coerce')
    data['Date'] = pd.to_datetime(data['datetime_str'], format="%d/%m/%Y, %I:%M %p", errors='coerce').dt.date
    data['Time'] = pd.to_datetime(data['datetime_str'], format="%d/%m/%Y, %I:%M %p", errors='coerce').dt.time
    data = data.dropna(subset=['datetime'])
    data = data.drop(columns=['datetime_str'])
    data = data.drop(columns=['datetime'])

    # Extract sender and message
    data[['sender', 'text_message']] = data['text_2'].str.split(': ', 1, expand=True)
    data = data.dropna(subset=['text_message'])
    data = data.drop(columns=['text', 'text_2'])

    ### changing datatype of "Date" column.
    data["Date"] = pd.to_datetime(data["Date"])
    data['Day'] = data['Date'].dt.weekday.map(weeks)

    ### Rearranging the columns for better understanding
    data = data[['Date', 'Day', 'Time', 'sender', 'text_message']]

    ### Changing the datatype of column "Day".
    data['Day'] = data['Day'].astype('category')

    # Improving the data ##2
    ### Counting number of letters in each message
    data['Letter'] = data['text_message'].apply(lambda s: len(s))
    ### Counting number of word's in each message
    data['Word'] = data['text_message'].apply(lambda s: len(s.split(' ')))

    ### Function to count number of links in dataset, it will add extra column and store information in it.
    URLPATTERN = r'(https?://\S+)'
    data['urlcount'] = data.text_message.apply(lambda x: re.findall(URLPATTERN, x)).str.len()

    ### Function to count number of media in chat.
    MEDIAPATTERN = r'<Media omitted>'
    data['Media_Count'] = data.text_message.apply(lambda x: re.findall(MEDIAPATTERN, x)).str.len()

    generateOutputData()



def about():
    messagebox.showinfo('WhatsApp Analyser', 'Welcome to WhatsApp Analyser')



def createNewWindow():
    ws = tk.Tk()
    width = ws.winfo_screenwidth()
    height = ws.winfo_screenheight()
    ws.geometry("%dx%d" % (width, height))
    ws.title('Feedback')
    font1 = font.Font(family='Georgia', size='22', weight='bold')
    label1 = Label(ws, text="Hey There! Welcome to WhatsApp Analyser. Please enter your feedback.", foreground="green3",font=font1)
    label1.pack(pady=5)
    e = tk.Text(ws, height=27, width=80)
    e.pack()
    b = Button(ws, text="SEND", width=10, command=callback)
    b.pack(pady=20)


def callback():
    inputText = e.get(1.0, "end-1c")


### Mostly Active Author in the Group
def ACTIVE_AUTHOR():
    A = plt.figure(figsize=(12, 8))#(6, 4)
    mostly_active = data['sender'].value_counts()
    ### Top 10 peoples that are mostly active in our Group is :
    m_a = mostly_active.head(10)
    bars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    x_pos = np.arange(len(bars))
    m_a.plot.bar()
    plt.xlabel('Sender', fontdict={'fontsize': 14, 'fontweight': 10})
    plt.ylabel('No. of messages', fontdict={'fontsize': 14, 'fontweight': 10})
    plt.title('Mostly active user in the group', fontdict={'fontsize': 20, 'fontweight': 8})
    plt.xticks(x_pos, bars)
    canvas = FigureCanvasTkAgg(A, frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=5, rowspan=10, columnspan=30,pady=50)
    generateOutputData()


#### Mostly Active Day in the Group
def ACTIVE_DAY():
    A = plt.figure(figsize=(12, 8))#(6, 4)
    A.patch.set_facecolor('white')
    active_day = data['Day'].value_counts()
    ### Top 10 peoples that are mostly active in our Group is :
    a_d = active_day.head(10)
    a_d.plot.bar()
    plt.xlabel('Day', fontdict={'fontsize': 14, 'fontweight': 10})
    plt.ylabel('No. of messages', fontdict={'fontsize': 14, 'fontweight': 10})
    plt.title('Mostly active day of week in the group', fontdict={'fontsize': 18, 'fontweight': 8})
    plt.gcf().subplots_adjust(bottom=0.25)
    canvas = FigureCanvasTkAgg(A, frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=5, rowspan=10, columnspan=30, pady=50)
    generateOutputData()



#### Time whenever our group is highly active
def HIGHLY_ACT():
    D = plt.figure(figsize=(12, 8))#(6, 4)
    D.patch.set_facecolor('white')
    t = data['Time'].value_counts().head(20)
    tx = t.plot.bar()
    tx.yaxis.set_major_locator(MaxNLocator(integer=True))  # Converting y axis data to integer
    plt.xlabel('Time', fontdict={'fontsize': 14, 'fontweight': 10})
    plt.ylabel('No. of messages', fontdict={'fontsize': 14, 'fontweight': 10})
    plt.title('Analysis of time when group was highly active.', fontdict={'fontsize': 18, 'fontweight': 8})
    plt.gcf().subplots_adjust(bottom=0.25)
    canvas = FigureCanvasTkAgg(D, frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=5, rowspan=10, columnspan=30,pady=50)
    generateOutputData()

#### Users with the maximum number of words in the message
def MAX_NUM():
    max_words = data[['sender', 'Word']].groupby('sender').sum()
    A = plt.figure(figsize=(12, 8))
    A.patch.set_facecolor('white')
    m_w = max_words['Word'].sort_values(ascending=False).head(10)
    bars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    x_pos = np.arange(len(bars))
    m_w.plot.bar()
    plt.xlabel('sender',fontdict={'fontsize': 14, 'fontweight': 10})
    plt.ylabel('No. of words',fontdict={'fontsize': 14, 'fontweight': 10})
    plt.title('Users with the maximum number of words in the group', fontdict={'fontsize': 18, 'fontweight': 8})
    plt.xticks(x_pos, bars)
    plt.gcf().subplots_adjust(bottom=0.25)
    canvas = FigureCanvasTkAgg(A, frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=5, rowspan=10, columnspan=30, pady=50)
    generateOutputData()


### Word Cloud of mostly used word in the Group
def wordCloud1():
    text = " ".join(review for review in data.text_message)
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color="white").generate(text)
    ### Display the generated image:
    A = plt.figure(figsize=(10, 5))
    A.patch.set_facecolor('white')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    canvas = FigureCanvasTkAgg(A, frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=10, column=5, columnspan=150, rowspan=20)
    generateOutputData()



### Report for the particular group message
def displayReport():
    gui_text_widget = scrolledtext.ScrolledText(frame, state="disabled", width=145, bd=0)
    gui_text_widget.grid(row=28, column=5, rowspan=15, columnspan=120, pady=100)
    global output
    for i in output:
        gui_text = i + '\n'
        # Set the Text widget's state to normal so that we can edit its text
        gui_text_widget.config(state="normal")
        # Insert the text at the end
        gui_text_widget.insert("end", gui_text)
        # Set the Text widget's state to disabled to disallow the user changing the text
        gui_text_widget.config(state="disabled")
    generateOutputData()


def clear():
    list = frame.grid_slaves()
    for l in list:
        l.destroy()


def clearOutput():
    clear()
    B = plt.figure(figsize=(6, 21))#20
    B.patch.set_facecolor('gray')
    canvas = FigureCanvasTkAgg(B, frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=4, rowspan=40)

    global output
    output.clear()
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()

    active_author = plt.figure(figsize=(12, 8))
    active_author.patch.set_facecolor('gray')
    canvas = FigureCanvasTkAgg(active_author, frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=5, rowspan=10, columnspan=30, pady=50)

    highly_act = plt.figure(figsize=(12, 8))
    highly_act.patch.set_facecolor('gray')
    canvas = FigureCanvasTkAgg(highly_act, frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=5, rowspan=10, columnspan=30, pady=50)

    active_day = plt.figure(figsize=(12, 8))
    active_day.patch.set_facecolor('gray')
    canvas = FigureCanvasTkAgg(active_day, frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=5, rowspan=10, columnspan=30, pady=50)

    max_num = plt.figure(figsize=(12, 8))
    max_num.patch.set_facecolor('gray')
    canvas = FigureCanvasTkAgg(max_num, frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=5, rowspan=10, columnspan=30, pady=50)

    wordcloud1 = plt.figure(figsize=(10, 5))
    wordcloud1.patch.set_facecolor('gray')
    canvas = FigureCanvasTkAgg(wordcloud1, frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=10, column=5, columnspan=150, rowspan=20)

    gui_text_widget = tk.Text(frame, state="disabled", width=110, bg='gray', bd=0)
    gui_text_widget.grid(row=28, column=5, rowspan=10, columnspan=120, pady=20)


def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))



try:
    import Tkinter as tk
except:
    import tkinter as tk


fileSelected = False
data = None
def open_file():
    global data
    fileSelected = True
    flag=0
    if (fileSelected == True):
        tf = filedialog.askopenfilename(
            initialdir="C:\\Users\\ASUS\PycharmProjects\pythonProject",
            title="Open Text file",
            filetypes=(("Text Files", "*.txt"),)
        )

    filename = tf.split('/')[-1]
    mostActiveAuthor['state'] = tk.NORMAL
    mostActiveDay['state'] = tk.NORMAL
    timeHighlyActive['state'] = tk.NORMAL
    maxNumOfWords['state'] = tk.NORMAL
    wordcloud['state'] = tk.NORMAL
    generateReport['state'] = tk.NORMAL
    feedback['state'] = tk.NORMAL
    pathh.insert(END, tf)
    data = pd.read_csv(filename, delimiter="\t", header=None, names=['text'])
    cleanData()



output = []


root = tk.Tk()
# getting screen width and height of display
width = 1920 #root.winfo_screenwidth()
height = 1080 #root.winfo_screenheight()
# setting tkinter window size
root.geometry("%dx%d" % (width, 2000))
root.title('WhatsApp Analyser page 1')

canvas = tk.Canvas(root, borderwidth=0, background='gray')
frame = tk.Frame(canvas, background='gray')
vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)

vsb.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((0, 0), window=frame, anchor="nw")

frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

### Menu Bar ###
menubar = Menu(root, background='#FFFFFF', foreground='black', activebackground='white', activeforeground='black')
file = Menu(menubar, tearoff=1, background='#FFFFFF', foreground='black')
file.add_command(label="New")
file.add_command(label="Open")
file.add_command(label="Save")
file.add_command(label="Save as")
file.add_separator()
file.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=file)

edit = Menu(menubar, tearoff=0)
edit.add_command(label="Undo")
edit.add_separator()
edit.add_command(label="Cut")
edit.add_command(label="Copy")
edit.add_command(label="Paste")
menubar.add_cascade(label="Edit", menu=edit)

help = Menu(menubar, tearoff=0)
help.add_command(label="About", command=about)
menubar.add_cascade(label="Help", menu=help)

root.config(menu=menubar)

B = plt.figure(figsize=(6, 20))
B.patch.set_facecolor('gray')
canvas = FigureCanvasTkAgg(B, frame)
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=0, columnspan=4, rowspan=100)

# Buttons
filebut = Button(root, text="SELECT FILE", justify='center', command=open_file, height=2, width=29, fg='black')
filebut.place(x=30, y=80)

reload = Button(root, text="RELOAD", justify='center', command=reloadData, height=2, width=6, fg='black')
reload.place(x=253, y=80)

feedback = Button(root, text="FEEDBACK", font=("Times bold", 14), justify='center', command=createNewWindow, height=2,width=170, fg='black',state=tk.DISABLED)
feedback.place(x=10, y=5)

pathh = Entry(root, width=45)
pathh.place(x=30, y=140)

mostActiveAuthor = tk.Button(root, text="MOST ACTIVE USER",height=2, width=38, command=ACTIVE_AUTHOR,fg='black',state=tk.DISABLED)
mostActiveAuthor.place(x=30, y=180)

mostActiveDay = Button(root, text="MOST ACTIVE DAY", height=2, width=38, command=ACTIVE_DAY, fg='black',state=tk.DISABLED)
mostActiveDay.place(x=30, y=230)

timeHighlyActive = Button(root, text=" TIME HIGHLY ACTIVE", height=2, width=38, command=HIGHLY_ACT, fg='black',state=tk.DISABLED)
timeHighlyActive.place(x=30, y=280)

maxNumOfWords = Button(root, text="MAX NUMBER OF WORDS", height=2, width=38, command=MAX_NUM, fg='black',state=tk.DISABLED)
maxNumOfWords.place(x=30, y=330)

wordcloud = Button(root, text="MOSTLY USED WORDS", height=2, width=38, command=wordCloud1, fg='black',state=tk.DISABLED)
wordcloud.place(x=30, y=380)

generateReport = Button(root, text="GENERATE REPORT", height=2, width=38, command=displayReport, fg='black',state=tk.DISABLED)
generateReport.place(x=30, y=430)

exitbutton = Button(root, text="EXIT", height=2, width=38, command=root.withdraw, fg='black')
exitbutton.place(x=30, y=480)

clearOutput()
root.mainloop()