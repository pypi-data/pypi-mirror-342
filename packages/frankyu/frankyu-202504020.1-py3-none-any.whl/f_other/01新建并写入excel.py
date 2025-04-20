#!/usr/bin/env python
# coding: utf-8

# In[1]:


import xlwings


# In[2]:


import frankyu


# In[3]:


import frankyu.excel


# In[4]:


ex = frankyu.excel


# In[5]:


app = ex.initialize_excel()


# In[6]:


book = ex.create_workbook(app)


# In[7]:


def excelpid():
        
    
    bbb = []
    for i in xlwings.apps:
        aaa =i.pid
        bbb.append(aaa)
        #print(bbb)
    app = xlwings.apps[bbb[0]]
    return app.pid
excelpid()


# In[ ]:





# In[8]:


eee = excelpid()


# In[9]:


rng =   xlwings.apps[eee].books[0].sheets[0].range("A1")
rng.value = "=2+3"


# In[10]:


xlwings.apps


# In[11]:


for i in xlwings.apps:
    print(i.pid)
    for j in i.books:
        print()
        print(j.name)


# In[12]:


rng.sheet.book.app.pid


# In[13]:


import time

time.sleep(4)


xlwings.apps[excelpid()].quit()


# In[ ]:




