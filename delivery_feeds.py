from string import Template
import os
import os.path
import time

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
now = time.localtime()

ROOT_PATH =  PROJECT_PATH

FEEDS_PATH = ROOT_PATH + '/' + 'feeds'
RECIPE_PATH = ROOT_PATH + '/' +'unofficial'

# lstfeed = ['latimes','nytimes','korea_herald','lwn']
# lstfeed = ['hani','joongangopinion','Kyunghyang','mediatoday','mk','presian','sisa',]
# lstfeed = ['mediatoday','presian','sisa',]


lstfeed = {"unofficial":['mediatoday','presian','sisa',],
           "official":['latimes','nytimes']}

lstfeed = {"unofficial":['presian'],
           "official":['latimes']}

s_now = str(now.tm_year) +  str(now.tm_mon) + str(now.tm_mday)

def main():
        fetch(lstfeed)
        send(lstfeed)

def fetch(feeds):
    print feeds , ' Fetching ...'
    cmd_temp = Template('ebook-convert $recipe_path/$recipe $output_path/$output_file')
    for key in feeds.keys():
        for value in feeds[key]:
            d = dict (recipe_path = ROOT_PATH + '/' + key,
                      recipe = value + '.recipe', 
                      output_path = FEEDS_PATH ,
                      output_file = value   + '_'+ s_now + ".mobi")
            cmd = cmd_temp.safe_substitute(d)

            print cmd
            os.system(cmd)

def send(feeds):
    print feeds, ' Sending ...'
    for key in feeds.keys():
        for value in feeds[key]:

            cmd_temp = Template('''calibre-smtp --attachment $output_path/$output_file \
    --relay smtp.gmail.com --port 587 \
    --username kd.pointer81 --password $password  \
    --encryption-method TLS kd.pointer81@gmail.com pointer81@free.kindle.com "" \
    ''')

            d = dict (recipe_path = ROOT_PATH + '/' + key,
                      recipe = value + '.recipe', 
                      password = "2345wert",
                      output_path = FEEDS_PATH ,
                      output_file = value  + '_'+ s_now + ".mobi")
    
            cmd = cmd_temp.safe_substitute(d)
            print cmd
            os.system(cmd)


if __name__ == "__main__":
    main()
