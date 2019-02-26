#!/usr/bin/env python
# coding: utf-8

# # PISA Data Exploration and Analysis
# ## by Lucy Todd
# 
# ## Preliminary Wrangling
# 
# > The data set I have chosen to use is the PISA 2012 assessment. I will be focussing on the effects and relationships of different factors on student maths scores in the United Kingdom and Japan.

# In[1]:


# import all packages and set plots to be embedded inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


#I'm now going to read in the raw data
df_pisa_uncut = pd.read_csv('pisa2012.csv', encoding = "ISO-8859-1")


# In[3]:


#For this investigation I will only be comparing the UK and Japan, so I am going to cut the dataset to make it smaller easier to investigate
df_pisa = df_pisa_uncut[(df_pisa_uncut.CNT == 'United Kingdom') | (df_pisa_uncut.CNT == 'Japan')].copy()


# In[4]:


#I will also import the dictionary that will tell me what the column headers mean
df_dict = pd.read_csv('pisa_dict.csv', encoding = "ISO-8859-1")


# ### What is the structure of your dataset?
# 
# > The pisa dataset is structured as a row of data for each student that took part. There are columns for their demographic data (such as country, gender, school), columns for their answers to the survey questions (such as spent doing homework) and their final scores in each of the tests they undertook.
# 
# > I will also be using the data dictionary that PISA provide in order to determine the names of different columns.
# 
# ### What is/are the main feature(s) of interest in your dataset?
# 
# > As this is such a huge dataset I have chosen to focus my exploration on two countries (Japan and the United Kingdom), and will be looking at the effects of different factors on student maths scores. I will be investigation the relationship between the way in which the students answer the survey questions, and their maths score. As well as the effect of gender and country on their survey answers and maths score.
# 
# ### What features in the dataset do you think will help support your investigation into your feature(s) of interest?
# 
# > I will be looking the the answers to the survey questions that each student answered. I will start with the questions on what technology each student has at home, and will go onto their participation in outside of school study to see the effect that this has on their maths score. To find each students maths score I will use the mean value of the 5 plausible values provided in the dataset. The plausible values are statistical imputations based on a predictive model to calculate each students score.

# In[5]:


#I am going to calculate the average of the plausible values to use the maths score for each student
df_pisa['maths score'] = df_pisa[['PV1MATH', 'PV2MATH', 'PV3MATH', 'PV4MATH', 'PV5MATH']].mean(axis = 1)


# In[6]:


#I also want to rename some of the columns I will be using to make them easier to understand
df_pisa = df_pisa.rename(columns = {'CNT':'country'})
df_pisa = df_pisa.rename(columns = {'ST04Q01':'gender'})
df_pisa = df_pisa.rename(columns = {'Unnamed: 0':'ID'})


# # Country

# ## <font color=dodgerblue>1.1 Average maths score by country</font>

# In[7]:


#I will find the mean maths score for each country
country_mean = df_pisa.groupby(['country']).mean()
country_mean.head()


# In[8]:


#I need to reset the index for this dataframe
country_mean.reset_index(inplace = True)


# In[9]:


#This is a bar chart of the average maths score of each country

sb.catplot(x='country', y='maths score', 
           data = country_mean, height=6, kind='bar', palette='muted')


# §

# # Gender

# ## <font color=dodgerblue>2.1 Average maths score by gender and country</font>

# In[10]:


#I will create a new datafram to look at the gender/country stats on their own
gender = df_pisa[['ID','country', 'gender', 'maths score']]


# In[11]:


#I will find the mean maths score for each country
gender_mean = gender.groupby(['country', 'gender']).mean()
gender_mean.head()


# In[12]:


#I need to reset the index for this dataframe
gender_mean.reset_index(inplace = True)


# In[13]:


#This is a bar chart of the average maths score of each country by gender
sb.catplot(x='country', y='maths score', hue = 'gender',
           data = gender_mean, height=6, kind='bar', palette='muted')


# <font color=dodgerblue>This is a bivariate plot to show the difference in the average maths score between males and females. It is also split by country. We can see that in both countries females have a lower average maths score than males, and that both UK males and females have a lower average score than the same gender in Japan.
# 
# It would be interesting to see the proportion of males and females in each quartile by maths score, for each country.</font>

# ## <font color=dodgerblue>2.2 Gender by maths score quartile (split by country)</font>

# In[14]:


#First I want to check the percentage of males and females in the sample for Japan and the UK, to make sure that this is a fair comparison
gender_Japan = gender[gender['country']=='Japan']
gender_UK = gender[gender['country']=='United Kingdom']

sorted_counts_J = gender_Japan['gender'].value_counts()
sorted_counts_UK = gender_UK['gender'].value_counts()

ax1 = plt.subplot2grid((2,2),(0,0))
plt.pie(sorted_counts_J, labels = sorted_counts_J.index, autopct='%1.1f%%', startangle = 90,
        counterclock = False);
plt.title('Japan')

ax1 = plt.subplot2grid((2,2), (0, 1))
plt.pie(sorted_counts_UK, labels = sorted_counts_UK.index, autopct='%1.1f%%', startangle = 90,
        counterclock = False);
plt.title('United Kingdom')


# <font color=dodgerblue>This first chart is a simple univariate plot, to show the proportion of males and females in each sample for Japan and the UK. The UK has almost 50/50 males and females. The Japan sample has slightly more males, so we should bare this in mind when we look at the gender quartiles.</font>

# In[15]:


#I am going to create two new dataframes. One with just the maths scores for Japan, and the other for the UK
gender_Japan = gender.loc[gender['country']=='Japan']
gender_UK = gender.loc[gender['country']=='United Kingdom']

#I now want to split each new dataframe into quartiles
quartiles_Japan = pd.qcut(gender_Japan['maths score'], 4, labels=['Q1','Q2','Q3','Q4'])
quartiles_UK = pd.qcut(gender_UK['maths score'], 4, labels=['Q1','Q2','Q3','Q4'])

#I will create a new column in each dataframe with the quartile label in it
gender_Japan = gender_Japan.assign(quartile=quartiles_Japan.values)
gender_UK = gender_UK.assign(quartile=quartiles_UK.values)

#I will create 4 new dataframes for Japan, separating by quartile now
Japan_Q1 = gender_Japan[(gender_Japan['quartile'] == "Q1")]
Japan_Q2 = gender_Japan[(gender_Japan['quartile'] == "Q2")]
Japan_Q3 = gender_Japan[(gender_Japan['quartile'] == "Q3")]
Japan_Q4 = gender_Japan[(gender_Japan['quartile'] == "Q4")]

#I will create 4 new dataframes for the UK, separating by quartile now
UK_Q1 = gender_UK[(gender_UK['quartile'] == "Q1")]
UK_Q2 = gender_UK[(gender_UK['quartile'] == "Q2")]
UK_Q3 = gender_UK[(gender_UK['quartile'] == "Q3")]
UK_Q4 = gender_UK[(gender_UK['quartile'] == "Q4")]


# In[16]:


#Now I can plot pie charts for each quartile to show the proportion of males to females for Japan
sorted_counts_1 = Japan_Q1['gender'].value_counts()
sorted_counts_2 = Japan_Q2['gender'].value_counts()
sorted_counts_3 = Japan_Q3['gender'].value_counts()
sorted_counts_4 = Japan_Q4['gender'].value_counts()

#first row, first col
ax1 = plt.subplot2grid((2,2),(0,0))
plt.pie(sorted_counts_1,labels = sorted_counts_1.index, autopct='%1.1f%%', startangle = 90,
        counterclock = False)
plt.title('Quartile 1')
#first row sec col
ax1 = plt.subplot2grid((2,2), (0, 1))
plt.pie(sorted_counts_2,labels = sorted_counts_2.index, autopct='%1.1f%%', startangle = 90,
        counterclock = False)
plt.title('Quartile 2')
#Second row first column
ax1 = plt.subplot2grid((2,2), (1, 0))
plt.pie(sorted_counts_3,labels = sorted_counts_3.index, autopct='%1.1f%%', startangle = 90,
        counterclock = False)
plt.title('Quartile 3')
#second row second column
ax1 = plt.subplot2grid((2,2), (1, 1))
plt.pie(sorted_counts_4,labels = sorted_counts_4.index, autopct='%1.1f%%', startangle = 90,
        counterclock = False)
plt.title('Quartile 4')


# <font color=dodgerblue>This is a univariate plot and shows the makeup of each quartile by maths score in Japan. We can see that the top 25% of maths scores are largely given by males, and the split becomes more even as you go down the quartiles. Quartile 1 and quartile 2 contain marginally more females than males.
#     
#  It should be noted that there are slightly more males than females in the Japan sample, however the 4th quartile still has significantly more boys in it.</font>

# In[17]:


#I can now do the same for the UK
sorted_counts_1 = UK_Q1['gender'].value_counts()
sorted_counts_2 = UK_Q2['gender'].value_counts()
sorted_counts_3 = UK_Q3['gender'].value_counts()
sorted_counts_4 = UK_Q4['gender'].value_counts()

#first row, first col
ax1 = plt.subplot2grid((2,2),(0,0))
plt.pie(sorted_counts_1,labels = sorted_counts_1.index, autopct='%1.1f%%', startangle = 90,
        counterclock = False)
plt.title('Quartile 1')
#first row sec col
ax1 = plt.subplot2grid((2,2), (0, 1))
plt.pie(sorted_counts_2,labels = sorted_counts_2.index, autopct='%1.1f%%', startangle = 90,
        counterclock = False)
plt.title('Quartile 2')
#Second row first column
ax1 = plt.subplot2grid((2,2), (1, 0))
plt.pie(sorted_counts_3,labels = sorted_counts_3.index, autopct='%1.1f%%', startangle = 90,
        counterclock = False)
plt.title('Quartile 3')
#second row second column
ax1 = plt.subplot2grid((2,2), (1, 1))
plt.pie(sorted_counts_4,labels = sorted_counts_4.index, autopct='%1.1f%%', startangle = 90,
        counterclock = False)
plt.title('Quartile 4')


# <font color=dodgerblue>The same graph for the UK shows that their quartiles are more evenly spli. As with Japaan, there are more males than females in the top two quartiles, and more females than males in the lower two quartiles.
# 
# I want to check the percentiles males and females in each country next.</font>

# In[18]:


gender_Japan[(gender_Japan['gender'] == "Male")]['maths score'].describe()


# In[19]:


gender_Japan[(gender_Japan['gender'] == "Female")]['maths score'].describe()


# In[20]:


gender_UK[(gender_UK['gender'] == "Male")]['maths score'].describe()


# In[21]:


gender_UK[(gender_UK['gender'] == "Female")]['maths score'].describe()


# <font color=dodgerblue>We can see that the male percentiles are consistently higher for males than females for each country. Meaning that males are scoring higher on average at each level.
# 
# Next I think it would be interesting to view this data as boxplots to look further into the distribution of boys and girls maths scores.</font>

# ## <font color=dodgerblue>2.3 Maths score box plots by gender and country</font>

# In[22]:


#I first need to create a new column that combines gender and country
a = gender["country"] + " - " + gender["gender"]
gender.is_copy = False
gender['gender - country'] = a
gender.head()


# In[23]:


#This is a box plot of maths scores by gender/country 
plt.figure(figsize = [30, 7])
base_color = sb.color_palette()[0]

plt.subplot(1, 2, 2)
sb.boxplot(data = gender, x = 'gender - country', y = 'maths score', color = base_color)


# <font color=dodgerblue>We can see from the box plot above that the group with the highest median maths score is Japan/male, then Japan/female, UK/male, UK/female.
# 
# The interquartile ranges for each group look fairly similar in size, meaning that for each group there is a similar amount of agreement between scores. The whiskers for each plot are also a similar size, but vary in upper and lower limits.
# 
# For each group there are quite a lot of lower outliers, however it is interesting that the UK plots have more outliers at the top. This may however be due to a larger sample size for the UK.</font>

# # Technology at home

# <font color=dodgerblue>In this section I want to look at the effect different technologies have on boys and girls respectively in each country.</font>

# In[24]:


#I will create a new dataframe that looks at country, gender, what technology is present in the students house, and their maths score
athome_tech = df_pisa[['country', 'gender', 'IC01Q01', 'IC01Q02', 'IC01Q03', 'IC01Q04', 'IC01Q05', 'IC01Q06', 'IC01Q07', 'IC01Q08', 'IC01Q09', 'IC01Q10', 'IC01Q11', 'maths score']]


# In[25]:


#I want to check the column names for the dictionary dataframe, as I need to check what the code stands for
df_dict.head()


# In[26]:


#I know that all of the technology at home columns start with the string 'IC01' so I will search for any code names in the dictionary that contain that and then print their long descriptions as a list
my_list = df_dict[df_dict['Unnamed: 0'].str.contains("IC01")]['x'].tolist()
print(my_list)


# In[27]:


#now I can rename the column headers in my new data fram so that I can see what they mean
athome_tech.columns = ['country', 'gender', 'Desktop Computer', 'Portable laptop', 'Tablet computer', 'Internet connection', 'Video games console', 'Cell phone w/o Internet', 'Cell phone with Internet', 'Mp3/Mp4 player', 'Printer', 'USB (memory) stick', 'Ebook reader', 'maths score']


# In[28]:


athome_tech.head(1)


# <font color=dodgerblue>It looks like there might not be any data for the UK in these columns, I will check this using the info function</font>

# In[29]:


athome_tech[athome_tech['country'] == 'United Kingdom'].info()


# <font color=dodgerblue>Unfortunately there is no data for at home technology for the UK, therefore I will have to focus this part of my analysis on Japan.</font>

# ## <font color=dodgerblue>3.1 Maths score by Video games usage and gender</font>

# In[30]:


#I want to calculate what the mean maths score for students that have/don't have a video games console is. I will group by country first, and then by the video games console column
video_games = athome_tech.groupby(['country','Video games console']).mean()
video_games.head()


# <font color=dodgerblue>The average maths score for students who have a video games console is higher than students who don't, regardless of whether they use it or not. Next I will look at this split down further by gender, as video games consoles may affect boys and girls differently.</font>

# In[31]:


athome_tech = athome_tech[athome_tech['country'] == "Japan"]


# In[32]:


#This time I am just looking at Japan, but I will also group by gender to see what the average maths score for males and females
video_games = athome_tech.groupby(['country','gender','Video games console']).mean()
video_games.head(6)


# In[33]:


#This dataframe is a multidex, I will need to reset the index before I can plot it as a graph
video_games.reset_index(inplace = True)


# In[34]:


#This is a bar chart of the average maths score of girls and boys, according to whether or not they have a video games console
sb.catplot(x='gender', y='maths score', hue='Video games console', 
           data = video_games, height=6, kind='bar', palette='muted')


# <font color=dodgerblue>The chart shows that for girls who use a video games console score on average less than girls who don't, however boys who use a video games console score on average in the middle of those who don't own one, and thos who do but don't use it.
# 
# The distinction here isn't especially clear, but it will be worthwhile looking at the effect of other technologies on boys and girls.</font>

# ## <font color=dodgerblue>3.2 Maths score by Internet usage and gender</font>

# In[35]:


#Now I will do the same for Internet connection
Internet = athome_tech.groupby(['country','gender','Internet connection']).mean()
Internet.head(6)


# In[36]:


Internet.reset_index(inplace = True)


# In[37]:


#This is a bar chart of the average maths score of girls and boys, according to whether or not they have an internet connection
g = sb.catplot(x='gender', y='maths score', hue='Internet connection', 
           data = Internet, height=6, kind='bar', palette='muted')


# <font color=dodgerblue>This is a much larger difference in score for males and females. Clearly, boys and girls who have internet connection and use it are by far in the lead in terms of average maths score. We could conclude that there is a correlation between using the internet at home and maths score. For both groups, those who don't have an internet connection score worse on average.
# 
# It would be interesting to look at the effect that internet usage on students phones has next.</font>

# ## <font color=dodgerblue>3.3 Maths score by type of phone by gender
# </font>
# 

# In[38]:


#Now I want to look at the effect of the two types of phones
phone_type = athome_tech.copy()


# In[39]:


phone_type.drop(['country', 'Desktop Computer', 'Portable laptop', 'Tablet computer', 'Internet connection','Video games console', 'Mp3/Mp4 player', 'Printer', 'USB (memory) stick', 'Ebook reader'], axis=1, inplace = True)
phone_type.head()


# In[40]:


#First I want to change all of the yes answers to just yes
phone_type['Cell phone w/o Internet'].replace('Yes, and I use it', 'Yes', inplace = True)
phone_type['Cell phone w/o Internet'].replace('Yes, but I dont use it', 'Yes', inplace = True)
phone_type['Cell phone with Internet'].replace('Yes, and I use it', 'Yes', inplace = True)
phone_type['Cell phone with Internet'].replace('Yes, but I dont use it', 'Yes', inplace = True)


# In[41]:


#Now I want to amalgamate the columns into one column 'phone type'
conditions = [
    (phone_type['Cell phone w/o Internet'] == 'Yes') & (phone_type['Cell phone with Internet'] == 'Yes'),
    (phone_type['Cell phone w/o Internet'] == 'Yes') & (phone_type['Cell phone with Internet'] == 'No'),
    (phone_type['Cell phone w/o Internet'] == 'No') & (phone_type['Cell phone with Internet'] == 'Yes')]
choices = ['both', 'no internet', 'internet']
phone_type['type'] = np.select(conditions, choices, default='no phone')


# In[42]:


#Now I want to find the mean score by gender and type of phone
phone_type_mean = phone_type.groupby(['gender','type']).mean()
phone_type_mean.head(8)


# In[43]:


#I need to reset the index in order to plot the graph
phone_type_mean.reset_index(inplace = True)


# In[44]:


#Now I can plot this as a bar graph
sb.catplot(x='gender', y='maths score', hue = 'type',
           data = phone_type_mean, height=6, kind='bar')


# <font color=dodgerblue>It is clear from this graph that studens who do not have a phone at all have a lower score on average than those who don't. The highest scoring group for each gender is having a phone with no internet. There is a smaller difference here between the next group, having a phone with internet. But we could conclude that there is a correlation between having access to internet on their phone and their maths score. In this case it is an inverse correlation, as students without internet on their phone score better.</font>

# ## <font color=dodgerblue>3.4 Maths score by type of computer by gender
# </font>

# In[45]:


#Now I want to look at the effect of different types of computer
computer_type = athome_tech.copy()


# In[46]:


computer_type.drop(['country', 'Cell phone w/o Internet', 'Cell phone with Internet', 'Internet connection','Video games console', 'Mp3/Mp4 player', 'Printer', 'USB (memory) stick', 'Ebook reader'], axis=1, inplace = True)
computer_type.head()


# In[47]:


#First I want to change all of the yes answers to just yes
computer_type['Desktop Computer'].replace('Yes, and I use it', 'Yes', inplace = True)
computer_type['Desktop Computer'].replace('Yes, but I dont use it', 'Yes', inplace = True)
computer_type['Portable laptop'].replace('Yes, and I use it', 'Yes', inplace = True)
computer_type['Portable laptop'].replace('Yes, but I dont use it', 'Yes', inplace = True)
computer_type['Tablet computer'].replace('Yes, and I use it', 'Yes', inplace = True)
computer_type['Tablet computer'].replace('Yes, but I dont use it', 'Yes', inplace = True)


# In[48]:


#Now I want to amalgamate the columns into one column 'type'
conditions = [
    (computer_type['Desktop Computer'] == 'Yes') & (computer_type['Portable laptop'] == 'No') & (computer_type['Tablet computer'] == 'No'),
    (computer_type['Desktop Computer'] == 'No') & (computer_type['Portable laptop'] == 'Yes') & (computer_type['Tablet computer'] == 'No'),
    (computer_type['Desktop Computer'] == 'No') & (computer_type['Portable laptop'] == 'No') & (computer_type['Tablet computer'] == 'Yes'),
    (computer_type['Desktop Computer'] == 'Yes') & (computer_type['Portable laptop'] == 'Yes') & (computer_type['Tablet computer'] == 'No'),
    (computer_type['Desktop Computer'] == 'Yes') & (computer_type['Portable laptop'] == 'No') & (computer_type['Tablet computer'] == 'Yes'),
    (computer_type['Desktop Computer'] == 'No') & (computer_type['Portable laptop'] == 'Yes') & (computer_type['Tablet computer'] == 'Yes'),
    (computer_type['Desktop Computer'] == 'Yes') & (computer_type['Portable laptop'] == 'Yes') & (computer_type['Tablet computer'] == 'Yes'),
    (computer_type['Desktop Computer'] == 'No') & (computer_type['Portable laptop'] == 'No') & (computer_type['Tablet computer'] == 'No')]
choices = ['Desktop computer','Laptop computer','Tablet','Multiple','Multiple','Multiple','Multiple','None']
computer_type['type'] = np.select(conditions, choices, default='None')


# In[49]:


computer_type['type'].value_counts()


# In[50]:


#Now I want to find the mean score by gender and type of computer
computer_type_mean = computer_type.groupby(['gender','type']).mean()
computer_type_mean.head(10)


# In[51]:


#I need to reset the index in order to plot the graph
computer_type_mean.reset_index(inplace = True)


# In[52]:


#Now I can plot this as a bar graph
sb.catplot(x='gender', y='maths score', hue = 'type',
           data = computer_type_mean, height=6, kind='bar')


# <font color=dodgerblue>It is clear from this graph that students who have no computer, or just a tablet on average score worse than those who have either a desktop, laptop, or multiple computers. This is true for males and females. It is interesting that those students who have a tablet score worse on average than students who have no computer at all.
# 
# It would be interesting to see the proportion of males and females who own each of these technologies. So far we have looked at the average scores of students who own them, but it would be interesting to see the extent to which each technology could affect each gender.</font>

# ## <font color=dodgerblue>3.5 Number of technology items by gender
# </font>

# In[53]:


#I am going to create a new dataframe to count the number of girls and boys that have each of the technologies at home
Japan_lollipop = athome_tech.copy()[athome_tech['country']=='Japan']
Japan_lollipop.head()


# In[54]:


#I will look at the possible values in each column
Japan_lollipop['Desktop Computer'].value_counts()


# In[55]:


#For students who have answeres 'yes but I don't use it' or ' yes and I use it' I will change their values to 1, for students who answered 'no' I will change their values to 0. This will allow me to count the number of students who answered yes
Japan_lollipop['Desktop Computer'].replace('Yes, and I use it', 1, inplace = True)
Japan_lollipop['Desktop Computer'].replace('Yes, but I dont use it', 1, inplace = True)
Japan_lollipop['Desktop Computer'].replace('No', 0, inplace = True)

Japan_lollipop['Portable laptop'].replace('Yes, and I use it', 1, inplace = True)
Japan_lollipop['Portable laptop'].replace('Yes, but I dont use it', 1, inplace = True)
Japan_lollipop['Portable laptop'].replace('No', 0, inplace = True)

Japan_lollipop['Tablet computer'].replace('Yes, and I use it', 1, inplace = True)
Japan_lollipop['Tablet computer'].replace('Yes, but I dont use it', 1, inplace = True)
Japan_lollipop['Tablet computer'].replace('No', 0, inplace = True)

Japan_lollipop['Internet connection'].replace('Yes, and I use it', 1, inplace = True)
Japan_lollipop['Internet connection'].replace('Yes, but I dont use it', 1, inplace = True)
Japan_lollipop['Internet connection'].replace('No', 0, inplace = True)

Japan_lollipop['Video games console'].replace('Yes, and I use it', 1, inplace = True)
Japan_lollipop['Video games console'].replace('Yes, but I dont use it', 1, inplace = True)
Japan_lollipop['Video games console'].replace('No', 0, inplace = True)

Japan_lollipop['Cell phone w/o Internet'].replace('Yes, and I use it', 1, inplace = True)
Japan_lollipop['Cell phone w/o Internet'].replace('Yes, but I dont use it', 1, inplace = True)
Japan_lollipop['Cell phone w/o Internet'].replace('No', 0, inplace = True)

Japan_lollipop['Cell phone with Internet'].replace('Yes, and I use it', 1, inplace = True)
Japan_lollipop['Cell phone with Internet'].replace('Yes, but I dont use it', 1, inplace = True)
Japan_lollipop['Cell phone with Internet'].replace('No', 0, inplace = True)

Japan_lollipop['Mp3/Mp4 player'].replace('Yes, and I use it', 1, inplace = True)
Japan_lollipop['Mp3/Mp4 player'].replace('Yes, but I dont use it', 1, inplace = True)
Japan_lollipop['Mp3/Mp4 player'].replace('No', 0, inplace = True)

Japan_lollipop['Printer'].replace('Yes, and I use it', 1, inplace = True)
Japan_lollipop['Printer'].replace('Yes, but I dont use it', 1, inplace = True)
Japan_lollipop['Printer'].replace('No', 0, inplace = True)

Japan_lollipop['USB (memory) stick'].replace('Yes, and I use it', 1, inplace = True)
Japan_lollipop['USB (memory) stick'].replace('Yes, but I dont use it', 1, inplace = True)
Japan_lollipop['USB (memory) stick'].replace('No', 0, inplace = True)

Japan_lollipop['Ebook reader'].replace('Yes, and I use it', 1, inplace = True)
Japan_lollipop['Ebook reader'].replace('Yes, but I dont use it', 1, inplace = True)
Japan_lollipop['Ebook reader'].replace('No', 0, inplace = True)


# In[56]:


#I am going to check that this worked
Japan_lollipop.head()


# In[57]:


#I am going to use this chart later on, so I want to create a copy of it now
Japan_heatmap = Japan_lollipop.copy()


# In[58]:


#For this graph I won't need 'country or maths score' so I will remove these columns
Japan_lollipop.drop(['country', 'maths score'], axis=1, inplace = True)


# In[59]:


#I want to check that the values are floats, so I will be able to add them together
Japan_lollipop.dtypes


# In[60]:


#I am going to groupby gender and then count for each column, this will give me the total number of males/females that own each technology
lollipop_counts = Japan_lollipop.groupby(['gender']).sum()
lollipop_counts.head()


# In[61]:


#I want to check how many males and females are in the sample overall, so I can calculate the proportions that own each technology
Japan_lollipop['gender'].value_counts()


# In[62]:


#I will set these values here so that I can use them in my calculations
Male_total = 3330
Female_total = 3021


# In[63]:


#I need to reset the index so I can use gender as a column
lollipop_counts.reset_index(inplace = True)


# In[64]:


#I want to create a separate dataframe for females so I can remove the gender column, and then carry out the calculation to find out the proportion
female_lollipop = lollipop_counts.loc[lollipop_counts['gender']=='Female']
female_lollipop.drop(['gender'], axis=1, inplace = True)


# In[65]:


#I will divide each value by the total number of females, then times by 100 to calculate the percentage. I can then add the gender column back in
female_lollipop = female_lollipop / Female_total
female_lollipop = female_lollipop * 100
female_lollipop['gender'] = 'Female'


# In[66]:


#Now I can carry out the exact same process for the male students
male_lollipop = lollipop_counts.loc[lollipop_counts['gender']=='Male']
male_lollipop.drop(['gender'], axis=1, inplace = True)


# In[67]:


#I will now calculate the proportions for males
male_lollipop = male_lollipop / Male_total
male_lollipop = male_lollipop * 100
male_lollipop['gender'] = 'Male'


# In[68]:


#I can now append the two separate dataframes back together
lollipop_percentages = male_lollipop.append(female_lollipop)
lollipop_percentages.head()


# In[69]:


#I need to rename all of the column headers to numbers, so that I can transpose the dataframe for the lollipop chart
lollipop_percentages.rename(index=str, columns={'Desktop Computer': '1',
 'Portable laptop': '2',
 'Tablet computer': '3',
 'Internet connection':'4',
 'Video games console':'5',
 'Cell phone w/o Internet':'6',
 'Cell phone with Internet':'7',
 'Mp3/Mp4 player':'8',
 'Printer':'9',
 'USB (memory) stick':'10',
 'Ebook reader':'11',
 'gender':'12',}, inplace = True)


# In[70]:


#I need to remove the gender column so that I can transpose the dataframe but keep all the values as floats
lollipop_percentages.drop(['12'], axis=1, inplace = True)


# In[71]:


#Now I can transpose the dataframe and set it as a new dataframe
lollipop_transpose = lollipop_percentages.transpose()


# In[72]:


#I want to check what it looks like
lollipop_transpose.head()


# In[73]:


#I want to create a list of the technology labels and then insert this back into the dataframe
row_labels = ('Desktop Computer','Portable laptop','Tablet computer','Internet connection','Video games console','Cell phone w/o Internet','Cell phone with Internet', 'Mp3/Mp4 player','Printer', 'USB (memory) stick','Ebook reader')


# In[74]:


#I want to add this list back on as a new column
lollipop_transpose['Technology'] = row_labels
lollipop_transpose.head()


# In[75]:


#Now I want to rename the column headers to male and female
lollipop_transpose.rename(index=str, columns={"1": "Male", "0": "Female"}, inplace = True)
lollipop_transpose.head()


# In[76]:


#Now I can create a lollipop chart of the proportion of males/females that own each specified technology
ordered_df = lollipop_transpose.sort_values(by='Male')
my_range=range(1,len(lollipop_transpose.index)+1)
 
import seaborn as sns
plt.hlines(y=my_range, xmin=ordered_df['Male'], xmax=ordered_df['Female'], color='grey', alpha=0.4)
plt.scatter(ordered_df['Male'], my_range, color='skyblue', alpha=1, label='Male')
plt.scatter(ordered_df['Female'], my_range, color='pink', alpha=0.4 , label='Female')
plt.legend()
 
# Add title and axis names
plt.yticks(my_range, ordered_df['Technology'])
plt.title("Proportion of males/females with specified technology", loc='left')
plt.xlabel('Percentage of gender')
plt.ylabel('Technology')


# <font color=dodgerblue>The lollipop chart shows the percentage of boys and girls who own each technology item. We can see that a higher proportion of girls own each of the technologies than boys respectively. This is not the case for video games consoles, where it is clear that boys are far more likely to own one than girls. Also, a higher proportion of boys own a USB stick. The technologies that most boys and girls own are a cell phone with intermet, internet connection and an Mp3/Mp4 player. Both genders are less likely to own a cell phone without internet, an Ebook reader or a tablet computer.
# 
# Laptop and desktop computer ownership is comparatively low, which is interesting when we think back to the graph of average maths score by computer ownership. Those students with a computer of some sort scored significantly higher than those without. Potentially if more students had access to a computer maths scores in general would increase.
# 
# Next it would be interesting to see technology ownership in general, and the number of technology items owned by each student.</font>

# ## <font color=dodgerblue>3.6 Number of technology items by maths score
# </font>

# In[77]:


#I am going to be using a dataframe that I created earlier on. If a student has a 1 it means they own the specified technology, if they have a 0 it means they do not
Japan_heatmap.head()


# In[78]:


list(Japan_heatmap)


# In[79]:


#I am going to create a new column of the total number of technology items each student owns, by adding together the individual technology columns
Japan_heatmap['Number of tech items'] = Japan_heatmap['Desktop Computer'] + Japan_heatmap['Portable laptop'] + Japan_heatmap['Tablet computer']+ Japan_heatmap['Internet connection']+ Japan_heatmap['Video games console']+ Japan_heatmap['Cell phone w/o Internet']+ Japan_heatmap['Cell phone with Internet']+ Japan_heatmap['Mp3/Mp4 player']+ Japan_heatmap['Printer']+ Japan_heatmap['USB (memory) stick']+ Japan_heatmap['Ebook reader']
Japan_heatmap.head()


# In[80]:


#I am going to put the maths scores into bins, I first need to find the lowest recorded score
Japan_heatmap['maths score'].max()


# In[81]:


#I also need to find the highest recorded score
Japan_heatmap['maths score'].min()


# In[82]:


#I will create an array of bins between 220 and 800, with bands of 10
bins = np.arange(220, 810, 10)


# In[83]:


#Now I am going to create a new column in my dataset to store the bins for each student
Japan_heatmap = Japan_heatmap.copy()
Japan_heatmap['binned'] = pd.cut(Japan_heatmap['maths score'], bins)


# In[84]:


#I want to be able to order these bins, so I need to store them as integers. I will fist split the string so that only the lower bound is showing, and then convert it into an integer
Japan_heatmap["binned"]= Japan_heatmap["binned"].astype(str) 
Japan_heatmap["binned2"]= Japan_heatmap["binned"].str.slice(1,4)
Japan_heatmap["binned2"]= Japan_heatmap["binned2"].astype(int)
Japan_heatmap.head()


# In[85]:


#I am going to create a pivot table to count the number of maths students in each bin, according to the number of tech items they have. It doesn't really matter what value I am counting, so I will use 'gender'
pivot = pd.pivot_table(Japan_heatmap, values='gender', index=['binned2'],
 columns=['Number of tech items'], aggfunc= 'size')
pivot.fillna(value=0, inplace = True)
pivot.head()


# In[86]:


#I am going to plot a heatmap, with number of tech items along the x axis and the maths score bin along the y axis. The colour axis represents the number of students in each square of the heatmap
plt.figure(figsize = [10, 7])
ax = sns.heatmap(pivot, linewidths=.2, cmap="YlGnBu")


# <font color=dodgerblue>This heatmap is a plot of all students, it has their number of tech items on the x axis  and their baths score bin along the y axis. The colour of each square shows the frequency of students in that square. So we can see that a lot of students own between 6 and 10 technology items at home, and most students have a maths score between 420 and 640.</font>

#  # Out of school study

# <font color=dodgerblue>In this next section I will be looking at the effect that various types of out of school study have on students in Japan and the UK. First I will look at the distribution of maths scores students who do and don't take part in various activities. </font>

# In[87]:


#I will create a new dataframe that looks at country, gender, out of school behaviour, and their maths score
athome_study = df_pisa[['country', 'gender', 'ST57Q01','ST57Q02','ST57Q03','ST57Q04','ST57Q05','ST57Q06', 'maths score']]


# In[88]:


#I want to check the column names for the dictionary dataframe, as I need to check what the code stands for
df_dict.head()


# In[89]:


#I know that all of the technology at home columns start with the string 'IC01' so I will search for any code names in the dictionary that contain that and then print their long descriptions as a list
my_list = df_dict[df_dict['Unnamed: 0'].str.contains('ST57Q')]['x'].tolist()
print(my_list)


# In[90]:


#now I can rename the column headers in my new data fram so that I can see what they mean
athome_study.columns = ['country', 'gender', 'Homework', 'Guided Homework', 'Personal Tutor', 'Commercial Company', 'With Parent', 'Computer', 'maths score']


# In[91]:


athome_study.head()


# ## <font color=dodgerblue>4.1 Difference in maths score between students who do and don't do homework by country
# </font>

# In[92]:


#For these charts I am only interested in whether or not someone participates in the activiy. I'm not interested in the number of hours they do. Therefore I will convert all hours about 0 to 1. This will make the next step easier
study_yesno = athome_study.copy()
study_yesno['Homework'].values[athome_study['Homework'].values > 0.0] = 1.0
study_yesno['Guided Homework'].values[athome_study['Guided Homework'].values > 0.0] = 1.0
study_yesno['Personal Tutor'].values[athome_study['Personal Tutor'].values > 0.0] = 1.0
study_yesno['Commercial Company'].values[athome_study['Commercial Company'].values > 0.0] = 1.0
study_yesno['With Parent'].values[athome_study['With Parent'].values > 0.0] = 1.0
study_yesno['Computer'].values[athome_study['Computer'].values > 0.0] = 1.0
study_yesno.head()


# In[93]:


#Now I can easily replace all 0s to 'No' and all 1s to 'Yes'
study_yesno['Homework'].replace(0.0, 'No', inplace = True)
study_yesno['Homework'].replace(1.0, 'Yes', inplace = True)

study_yesno['Guided Homework'].replace(0.0, 'No', inplace = True)
study_yesno['Guided Homework'].replace(1.0, 'Yes', inplace = True)

study_yesno['Personal Tutor'].replace(0.0, 'No', inplace = True)
study_yesno['Personal Tutor'].replace(1.0, 'Yes', inplace = True)

study_yesno['Commercial Company'].replace(0.0, 'No', inplace = True)
study_yesno['Commercial Company'].replace(1.0, 'Yes', inplace = True)

study_yesno['With Parent'].replace(0.0, 'No', inplace = True)
study_yesno['With Parent'].replace(1.0, 'Yes', inplace = True)

study_yesno['Computer'].replace(0.0, 'No', inplace = True)
study_yesno['Computer'].replace(1.0, 'Yes', inplace = True)


# In[94]:


#I want to create 6 new columns that I will use for the box plots. I need to concatenate the country with the column that tells us whether or not they participate in this activity
study_yesno['country - Homework'] = study_yesno["country"] + " - " + study_yesno["Homework"]
study_yesno['country - Guided Homework'] = study_yesno["country"] + " - " + study_yesno["Guided Homework"]
study_yesno['country - Personal Tutor'] = study_yesno["country"] + " - " + study_yesno["Personal Tutor"]
study_yesno['country - Commercial Company'] = study_yesno["country"] + " - " + study_yesno["Commercial Company"]
study_yesno['country - With Parent'] = study_yesno["country"] + " - " + study_yesno["With Parent"]
study_yesno['country - Computer'] = study_yesno["country"] + " - " + study_yesno["Computer"]

study_yesno.head()


# In[95]:


#Now I can plot a boxplot to show the difference in maths score between Japanese and UK students or do and don't do homework
plt.figure(figsize = [30, 7])
base_color = sb.color_palette()[0]

plt.subplot(1, 2, 2)
sb.boxplot(data = study_yesno, x = 'country - Homework', y = 'maths score', color = base_color)


# <font color=dodgerblue>From this chart we can see that those students who do homework in Japan and the UK have a higher median maths score than those who don't. The interquartile range for all four groups is very similar. The median value for students who do homework in the United Kingdom is only slightly higher than the median for students in Japan who don't do homework.</font>

# ## <font color=dodgerblue>4.2 Difference in maths score between students do and don't have a personal tutor by country
# </font>

# In[96]:


#I can plot the same chart for the other variables
plt.figure(figsize = [30, 7])
base_color = sb.color_palette()[0]

plt.subplot(1, 2, 2)
sb.boxplot(data = study_yesno, x = 'country - Personal Tutor', y = 'maths score', color = base_color)


# <font color=dodgerblue>From this chart we can see that grouping students by those who do and don't have a personal tutor has the opposite effect. For both the United Kingdom and Japan, those students who don't have a personal tutor have a higher median and lower and upper quartile.
# 
# In Japan the difference in median between those who do and don't have a tutor is particularly large.</font>

# ## <font color=dodgerblue>4.3 Difference in maths score between students who do and don't study with a parent by country
# </font>

# In[97]:


plt.figure(figsize = [30, 7])
base_color = sb.color_palette()[0]

plt.subplot(1, 2, 2)
sb.boxplot(data = study_yesno, x = 'country - With Parent', y = 'maths score', color = base_color)


# <font color=dodgerblue>The effect is similar if students who do and don't study with a parent are grouped together. Those that do have a higher median maths score and upper and lower quartile. However, the difference here is smaller.
# 
# I will now investigate for each country whether there is a correlation between the number of hours a student takes part in each activity, and their maths score.</font>

# ## <font color=dodgerblue>4.4 Maths score by hours spent on homework and country
# </font>

# In[98]:


sns.lmplot(x="Homework", y="maths score", hue="country",col='gender', data=athome_study, x_estimator=np.mean)


# <font color=dodgerblue>From this graph we can see that there is a positive correlation between the number of hours homework a student does, and their maths score. Thisis is true for girls and boys in Japan and the United Kingdom.
# 
# This regression plot shows the mean maths score for each number of hours of homework.</font>

# ## <font color=dodgerblue>4.5 Maths score by hours spent on homework with a parent and country
# </font>

# In[99]:


sns.lmplot(x="With Parent", y="maths score", hue="country",col='gender', data=athome_study, x_estimator=np.mean)


# <font color=dodgerblue>This regression plot shows that there is a negative correlation between the number of hours spent studying with a parent and maths score. The only exception is girls in Japan where there doesn't seem to be any correlation. It is important to note that correlation does not mean that doing homework with a parent causes a student to have a lower maths score.</font>

# ## <font color=dodgerblue>4.6 Maths score by total hours of study and country and gender
# </font>

# In[100]:


#I want to look at the total hours of study as well, so I will create a new column that is the sum of the hours spent on each activity
athome_study['total study'] = athome_study['Homework'] + athome_study['Guided Homework'] + athome_study['Personal Tutor'] + athome_study['Commercial Company'] + athome_study['With Parent'] + athome_study['Computer']


# In[101]:


sns.lmplot(x="total study", y="maths score", hue="country",col='gender', data=athome_study, x_estimator=np.mean)


# <font color=dodgerblue>This regression plot shows that there is a positive correlation between the number of hours of study a student does and their maths score. The correlation is stronger for students in Japan than in the UK.
# </font>

# ## <font color=dodgerblue>4.7 Total hours of study by maths score range and country
# </font>

# <font color=dodgerblue>In this section I want to investigate the number frequency of students by maths score and number of hours of out of school study</font>

# In[102]:


#Using the same method as earlier, I am going to separate the maths scores into bins
athome_study = athome_study.copy()
athome_study['score_binned'] = pd.cut(athome_study['maths score'], bins)
athome_study.head()


# In[103]:


#I want to be able to order these bins, so I need to store them as integers. I will fist split the string so that only the lower bound is showing, and then convert it into an integer
athome_study["score_binned"]= athome_study["score_binned"].astype(str) 
athome_study["score_binned2"]= athome_study["score_binned"].str.slice(1,4)
athome_study.head()


# In[104]:


#I want to create two different charts for the UK and Japan, so I will create two different dataframes now
athome_study_J = athome_study[athome_study['country'] == 'Japan']
athome_study_UK = athome_study[athome_study['country'] == 'United Kingdom']


# In[105]:


#I am going to create two pivot tables to count the number of maths students in each bin for each country, according to the number of hours of study they do It doesn't really matter what value I am counting, so I will use 'gender'
pivot_Japan = pd.pivot_table(athome_study_J, values='gender', index=['score_binned2'],
 columns=['Homework'], aggfunc= 'size')
pivot_Japan.fillna(value=0, inplace = True)

pivot_UK = pd.pivot_table(athome_study_UK, values='gender', index=['score_binned2'],
 columns=['Homework'], aggfunc= 'size')
pivot_UK.fillna(value=0, inplace = True)


# In[106]:


#Now I can plot two heatmaps side by side
plt.figure(figsize = [30, 7])
f, axes = plt.subplots(1, 2)
ax = sns.heatmap(pivot_Japan, linewidths=.2, cmap="YlGnBu",ax=axes[0]).set_title('Japan')
ax = sns.heatmap(pivot_UK, linewidths=.2, cmap="YlGnBu",ax=axes[1]).set_title('United Kingdom')


# <font color=dodgerblue>From this chart we can see that for the UK there is a high frequency of students who do between 0 and 9 hours homework, and have a score between 320 and 560. For Japan the frequenc is much smaller, however this is because the sample size for Japan is much smaller.</font>

# ## <font color=dodgerblue>4.8 Average hours of study by gender and country
# </font>

# <font color=dodgerblue>I want to look at the average number of hours of study that males and females do for each country.</font>

# In[107]:


#I want to look at the relationship between the total hours of study and the mean maths score for girls and boys, according to country. I am going to create a new dataframe to find the mean number of total study hours for girls and boys in each country
mean_study_time = athome_study.groupby(['country','gender']).mean()
mean_study_time.head()


# In[108]:


#I need to reset the index in order to plot a bar graph
mean_study_time.reset_index(inplace=True)


# In[109]:


#I can now plot a bar chart to show the mean number of study hours for boys and girls in Japan and the UK
sb.catplot(x='country', y='total study', hue = 'gender',
           data = mean_study_time, height=6, kind='bar', palette='muted')


# <font color=dodgerblue>We can see from this chart that female students in the UK do the most hours of study on average. Female students do more hours of study on average than males in both countries, and students in Japan do less hours of study as a whole than UK students.  </font>

# ## <font color=dodgerblue>4.9 Average maths score by gender, country and total hours of study
# </font>

# <font color=dodgerblue>I will now separte the hours of study out into bins, and look at the average maths score for boys and girls in each bin for both countries.</font>

# In[110]:


#It would be useful to group the study hours into bins, first I need to find the maximum number of hours
athome_study['total study'].max()


# In[111]:


#And the minimum
athome_study['total study'].min()


# In[112]:


#I will cut the datafram into bins
athome_study['total_study_binned'] = pd.cut(athome_study['total study'], [0,  10 , 20 , 30, 40], labels=['0-10',  '10-20'  ,'20-30', 'more than 30'])


# In[113]:


#Now I can create another dataframe to calculate the mean for each range of study hours, according to gender and country
mean_score_by_time = athome_study.groupby(['country','gender','total_study_binned']).mean()
mean_score_by_time.head(48)


# In[114]:


#I need to reset the index in order to plot this as a chart
mean_score_by_time.reset_index(inplace=True)


# In[115]:


#Now I can plot a bar chart to show the mean maths score according to each range of study hours
sb.catplot(x='total_study_binned', y='maths score', hue = 'gender', col = 'country',
           data = mean_score_by_time, height=6, kind='bar')


# <font color=dodgerblue>From this chart you can see that the average maths score increases for students as the bins increase. Interestingly, in Japan when students are doing over 20 hours of study a week, female students have a higher maths score on average. This is the opposite from all the other bins, where males have a higher average score for both countries.</font>

# ## <font color=dodgerblue>4.10 Proportion of students who participate in out of school study by gender and country
# </font>

# <font color=dodgerblue>It would be interesting to see the proportion of males and females who take part in each out of school study respectively, for each country.</font>

# In[116]:


#I will create a new dataframe for this analysis
study_lollipop = athome_study.copy()


# In[117]:


#I won't need the following columns so I am going to drop them
study_lollipop.drop(['total study', 'score_binned', 'score_binned2', 'total_study_binned', 'maths score'], axis=1, inplace = True)
study_lollipop.head()


# In[118]:


#If a student has answered Nan for the number of hours they spend on each activity I am going to marke them as 0 hours
study_lollipop = study_lollipop.replace(np.NaN, 0)


# In[119]:


#I want to be able to count the number of students who do and don't take part in each activity. Therefore if they answered 1 hour or more I will just mark them as 1, and if they answered 0 hours I will leave them as 0
study_lollipop['Homework'].values[study_lollipop['Homework'].values > 0.0] = 1.0
study_lollipop['Guided Homework'].values[study_lollipop['Guided Homework'].values > 0.0] = 1.0
study_lollipop['Personal Tutor'].values[study_lollipop['Personal Tutor'].values > 0.0] = 1.0
study_lollipop['Commercial Company'].values[study_lollipop['Commercial Company'].values > 0.0] = 1.0
study_lollipop['With Parent'].values[study_lollipop['With Parent'].values > 0.0] = 1.0
study_lollipop['Computer'].values[study_lollipop['Computer'].values > 0.0] = 1.0


# In[120]:


#Now I need to split the dataframe into two dataframes, one for each country
study_lollipop_J = study_lollipop[study_lollipop['country']=='Japan']
study_lollipop_UK = study_lollipop[study_lollipop['country']=='United Kingdom']


# In[121]:


#I am going to groupby gender and then count for each column, this will give me the total number of males/females that take part in each activity
lollipop_counts_J = study_lollipop_J.groupby(['gender']).sum()
lollipop_counts_UK = study_lollipop_UK.groupby(['gender']).sum()


# In[122]:


lollipop_counts_J.head()


# In[123]:


lollipop_counts_UK.head()


# In[124]:


#I want to check how many males and females are in the sample overall, so I can calculate the proportions that take part in each activity
study_lollipop_J['gender'].value_counts()


# In[125]:


#Now I will do the same for the UK
study_lollipop_UK['gender'].value_counts()


# In[126]:


#I will set these values here so that I can use them in my calculations
Male_total_J = 3330
Female_total_J = 3021
Male_total_UK = 6351
Female_total_UK = 6308


# In[127]:


#I need to reset the index so I can use gender as a column
lollipop_counts_J.reset_index(inplace = True)
lollipop_counts_UK.reset_index(inplace = True)


# In[128]:


#I need to split each dataframe again, this time by gender. I now have 4 different dataframes
lollipop_counts_J_F = lollipop_counts_J.loc[lollipop_counts_J['gender']=='Female']
lollipop_counts_J_F.drop(['gender'], axis=1, inplace = True)

lollipop_counts_J_M = lollipop_counts_J.loc[lollipop_counts_J['gender']=='Male']
lollipop_counts_J_M.drop(['gender'], axis=1, inplace = True)

lollipop_counts_UK_F = lollipop_counts_UK.loc[lollipop_counts_UK['gender']=='Female']
lollipop_counts_UK_F.drop(['gender'], axis=1, inplace = True)

lollipop_counts_UK_M = lollipop_counts_UK.loc[lollipop_counts_UK['gender']=='Male']
lollipop_counts_UK_M.drop(['gender'], axis=1, inplace = True)


# In[129]:


#I am going to divide each column by the total number of males/females, and then multiply by 100 to give me the percentage of students in that group who take part in that activity
lollipop_counts_J_F = lollipop_counts_J_F / Female_total_J
lollipop_counts_J_F = lollipop_counts_J_F * 100
lollipop_counts_J_F['gender'] = 'Female'

lollipop_counts_J_M = lollipop_counts_J_M / Male_total_J
lollipop_counts_J_M = lollipop_counts_J_M * 100
lollipop_counts_J_M['gender'] = 'Male'

lollipop_counts_UK_F = lollipop_counts_UK_F / Female_total_UK
lollipop_counts_UK_F = lollipop_counts_UK_F * 100
lollipop_counts_UK_F['gender'] = 'Female'

lollipop_counts_UK_M = lollipop_counts_UK_M / Male_total_UK
lollipop_counts_UK_M = lollipop_counts_UK_M * 100
lollipop_counts_UK_M['gender'] = 'Male'


# In[130]:


#Now I will join two gender dataframes together, so I have a percentage dataframe for each country
lollipop_percentages_Japan = lollipop_counts_J_F.append(lollipop_counts_J_M)
lollipop_percentages_UK = lollipop_counts_UK_F.append(lollipop_counts_UK_M)


# In[131]:


lollipop_percentages_Japan.head()


# In[132]:


lollipop_percentages_UK.head()


# In[133]:


#I need to drop the gender column so I can transpose the dataframe
lollipop_percentages_Japan.drop(['gender'], axis=1, inplace = True)
lollipop_percentages_UK.drop(['gender'], axis=1, inplace = True)


# In[134]:


lollipop_percentages_Japan_transpose = lollipop_percentages_Japan.transpose()
lollipop_percentages_UK_transpose = lollipop_percentages_UK.transpose()


# In[135]:


lollipop_percentages_Japan_transpose.head()


# In[136]:


lollipop_percentages_UK_transpose.head()


# In[137]:


#I need to reset the index so I can put the types of study into their own column
lollipop_percentages_Japan_transpose.reset_index(inplace=True)
lollipop_percentages_UK_transpose.reset_index(inplace=True)


# In[138]:


#Now I can rename the column headers
lollipop_percentages_Japan_transpose= lollipop_percentages_Japan_transpose.rename(index=str, columns={"index": "Out of school study", 0: "Female",1: "Male"})
lollipop_percentages_UK_transpose = lollipop_percentages_UK_transpose.rename(index=str, columns={"index": "Out of school study", 0: "Female", 1: "Male"})


# In[139]:


lollipop_percentages_Japan_transpose.head()


# In[140]:


lollipop_percentages_UK_transpose.head()


# In[141]:


#Now I can create a lollipop chart of the proportion of males/females that takepart in each activity
ordered_df = lollipop_percentages_Japan_transpose
my_range=range(1,len(lollipop_percentages_Japan_transpose.index)+1)
 
import seaborn as sns
plt.hlines(y=my_range, xmin=ordered_df['Male'], xmax=ordered_df['Female'], color='grey', alpha=0.4)
plt.scatter(ordered_df['Male'], my_range, color='skyblue', alpha=1, label='Male')
plt.scatter(ordered_df['Female'], my_range, color='pink', alpha=0.4 , label='Female')
plt.legend()
 
# Add title and axis names
plt.yticks(my_range, ordered_df['Out of school study'])
plt.title("Proportion of males/females in Japan who take part in out of school study", loc='left')
plt.xlabel('Percentage of gender')
plt.ylabel('Out of school study')


# In[142]:


#I will now do the same for the United Kingdom
ordered_df = lollipop_percentages_UK_transpose
my_range=range(1,len(lollipop_percentages_UK_transpose.index)+1)
 
import seaborn as sns
plt.hlines(y=my_range, xmin=ordered_df['Male'], xmax=ordered_df['Female'], color='grey', alpha=0.4)
plt.scatter(ordered_df['Male'], my_range, color='skyblue', alpha=1, label='Male')
plt.scatter(ordered_df['Female'], my_range, color='pink', alpha=0.4 , label='Female')
plt.legend()
 
# Add title and axis names
plt.yticks(my_range, ordered_df['Out of school study'])
plt.title("Proportion of males/females in the United Kingdom who take part in out of school study", loc='left')
plt.xlabel('Percentage of gender')
plt.ylabel('Out of school study')


# <font color=dodgerblue>From these two charts we can see that around 60% of students in all four groups do homework outside of school.
# 
# In the UK guided homework, homework with a parent and homework on a computer are far more common than in Japan.
# 
# In Japan there is not a lot of difference between the proportion of girls and boys who do home work with a personal tutor, commercial company or computer. In the UK a higher proportion of girls take part in all of these activities than boys respectively.
# 
# Aside from this, for Japan and the UK more girls proportionally take part in all of the out of school study activities than boys.</font>

# In[ ]:




