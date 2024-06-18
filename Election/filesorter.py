#%%
import os, shutil
#%%
path = r"C:\Users\Stroodles\Downloads\Modding"
#%%
os.listdir(path)
#%%
folder_names = ['Spreadsheets', 'Images', 'Documents']
#%%
for folder in folder_names:
    if not os.path.exists(path + "\\" + folder):
        os.mkdir(path + "\\" + folder)
# %%
for file in os.listdir(path):
    if file.endswith('.xlsx') or file.endswith('.xls') or file.endswith('.csv'):
        shutil.move(path + "\\" + file, path + "\\Spreadsheets\\" + file)
    elif file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
        shutil.move(path + "\\" + file, path + "\\Images\\" + file)
    elif file.endswith('.docx') or file.endswith('.pdf') or file.endswith('.txt'):
        shutil.move(path + "\\" + file, path + "\\Documents\\" + file)
# %%
os.listdir(path)