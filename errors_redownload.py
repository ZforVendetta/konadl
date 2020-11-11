import os
import re
import requests
import threading

'''
put "errors.log"  this file into same folder

run this file

it will try to redownload them

all downloaded images are saved in 'redownload' folder(you can change the value of store_path)

enjoy
'''


count_success = 0
count_fail = 0
count_exist = 0

def download_file(url, store_path):
    #get file name from url
    filename_url = url.split("/")[-1]
    filename = re.sub('%\d\d','_',filename_url).replace('_-_','_')
    #if file exists skip
    if os.path.exists(store_path+filename):
        global count_exist
        print(filename+'File exists, skip!')
        count_exist += 1
        return
    
    filepath = os.path.join(store_path, filename)
    file_data = requests.get(url, allow_redirects=True).content
    with open(filepath, 'wb') as handler:
        handler.write(file_data)
    print(filename+'\nsaved')


store_path = '.\\redownload\\'
if not os.path.exists(store_path):
    os.mkdir(store_path)

#by chaging value to change search keyword
keyword = "URL=https:"

#by changing file to change target file
search_target_file = open("./errors.log")
#output file
result_output_file = open("./redownload_result.log", "w",encoding='UTF-8')
#read the first line in the target file
line = search_target_file.readline()
#read content is not empty
while line:
    #print(line, end = '')    #print all lines
    if keyword in line:
        #print(line)    #print line contents keywords
        #write into result file
        #result_output_file.write(line)
        url = line.replace('URL=https:','https:').replace('\n','')
        
        try:
            download_file(url, store_path)
            count_success += 1
        except Exception as e:
            print(e)
            result_output_file.write(f'Error!{url}\n{e}\n')
            count_fail += 1
    #read the next line
    line = search_target_file.readline() 
msg = f'success:{count_success},skip:{count_exist},fail:{count_fail}'
result_output_file.write(msg)
print(msg)
search_target_file.close()
result_output_file.close()
