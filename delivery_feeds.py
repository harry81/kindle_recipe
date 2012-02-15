from string import Template
import os
import os.path
import time

now = time.localtime()

ROOT_PATH = os.getenv("HOME") + '/work/kindle_recipe'

FEEDS_PATH = ROOT_PATH + '/' + 'feeds'
RECIPE_PATH = ROOT_PATH + '/' +'official'

lstfeed = ['latimes','nytimes','korea_herald','lwn']

s_now = str(now.tm_year) +  str(now.tm_mon) + str(now.tm_mday)

def main():
    for lst in lstfeed:
        recipe = lst + '.recipe'
        fetch(recipe)
        send(recipe)

def fetch(m_recipe):
    print m_recipe , ' Fetching ...'
    cmd_temp = Template('ebook-convert $recipe_path/$recipe $output_path/$output_file')
    d = dict (recipe_path = RECIPE_PATH,
              recipe = m_recipe, 
              output_path = FEEDS_PATH ,
              output_file = m_recipe.split('.')[0]   + '_'+ s_now + ".mobi")
    cmd = cmd_temp.safe_substitute(d)

    #print cmd
    os.system(cmd)

def send(m_recipe):
    print m_recipe , ' Sending ...'
    cmd_temp = Template('''calibre-smtp --attachment $output_path/$output_file \
    --relay smtp.gmail.com --port 587 \
    --username kd.pointer81 --password $password  \
    --encryption-method TLS kd.pointer81@gmail.com pointer81@free.kindle.com "" \
    ''')

    d = dict (recipe_path = RECIPE_PATH,
              recipe = m_recipe,
              password = "2345wert",
              output_path = FEEDS_PATH ,
              output_file = m_recipe.split('.')[0]   + '_'+ s_now + ".mobi")
    
    cmd = cmd_temp.safe_substitute(d)
    #print cmd
    os.system(cmd)

    # cmd_temp = Template('rm $output_path/$output_file')
    # cmd = cmd_temp.safe_substitute(d)
    # print cmd
    # os.system(cmd)

if __name__ == "__main__":
    main()
