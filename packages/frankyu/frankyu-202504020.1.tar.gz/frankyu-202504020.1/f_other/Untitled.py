#!/usr/bin/env python
# coding: utf-8

# In[4]:


import f_other.install_jupyterlab_language_pack  as  ins


# In[8]:


ins.check_package_version("frankyu",pip_location=r"C:\Users\Public\Python314\Scripts\pip.exe")


# In[16]:


ins.execute_command([r"C:\Users\Public\Python314\Scripts\pip.exe","install",'--upgrade',  'frankyu'])


# In[ ]:


ins

