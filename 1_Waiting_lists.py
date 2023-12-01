import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

###########################################
# Loading inputs : users list
###########################################

df_waiting_list = pd.read_csv('./0_Users_list.csv', sep=';', encoding='utf-8', decimal='.')

###########################################
# Checking User id : empty and duplicates
###########################################

empty_user_idx = df_waiting_list[df_waiting_list['Vehicle_Id'].isnull()].index
df_waiting_list.drop(empty_user_idx , inplace=True)
df_waiting_list.reset_index(drop=True, inplace=True)

strict_duplicates = df_waiting_list[df_waiting_list.duplicated(subset=['Vehicle_Id'], keep='first')].index
df_waiting_list.drop(strict_duplicates , inplace=True)
df_waiting_list.reset_index(drop=True, inplace=True)

###########################################
# Marging data : max duration bewteen requested and suggested
###########################################

df_waiting_list['Duration_hours_monday_morning'] = df_waiting_list[['Duration_hours_suggested_monday_morning', 'Duration_hours_required_monday_morning']].max(axis=1)
df_waiting_list['Duration_hours_tuesday_morning'] = df_waiting_list[['Duration_hours_suggested_tuesday_morning', 'Duration_hours_required_tuesday_morning']].max(axis=1)
df_waiting_list['Duration_hours_wednesday_morning'] = df_waiting_list[['Duration_hours_suggested_wednesday_morning', 'Duration_hours_required_wednesday_morning']].max(axis=1)
df_waiting_list['Duration_hours_thursday_morning'] = df_waiting_list[['Duration_hours_suggested_thursday_morning', 'Duration_hours_required_thursday_morning']].max(axis=1)
df_waiting_list['Duration_hours_friday_morning'] = df_waiting_list[['Duration_hours_suggested_friday_morning', 'Duration_hours_required_friday_morning']].max(axis=1)

df_waiting_list['Duration_hours_monday_afternoon'] = df_waiting_list[['Duration_hours_suggested_monday_afternoon', 'Duration_hours_required_monday_afternoon']].max(axis=1)
df_waiting_list['Duration_hours_tuesday_afternoon'] = df_waiting_list[['Duration_hours_suggested_tuesday_afternoon', 'Duration_hours_required_tuesday_afternoon']].max(axis=1)
df_waiting_list['Duration_hours_wednesday_afternoon'] = df_waiting_list[['Duration_hours_suggested_wednesday_afternoon', 'Duration_hours_required_wednesday_afternoon']].max(axis=1)
df_waiting_list['Duration_hours_thursday_afternoon'] = df_waiting_list[['Duration_hours_suggested_thursday_afternoon', 'Duration_hours_required_thursday_afternoon']].max(axis=1)
df_waiting_list['Duration_hours_friday_afternoon'] = df_waiting_list[['Duration_hours_suggested_friday_afternoon', 'Duration_hours_required_friday_afternoon']].max(axis=1)

df_waiting_list.drop(['Duration_hours_suggested_monday_morning',
       'Duration_hours_suggested_tuesday_morning',
       'Duration_hours_suggested_wednesday_morning',
       'Duration_hours_suggested_thursday_morning',
       'Duration_hours_suggested_friday_morning',
       'Duration_hours_suggested_monday_afternoon',
       'Duration_hours_suggested_tuesday_afternoon',
       'Duration_hours_suggested_wednesday_afternoon',
       'Duration_hours_suggested_thursday_afternoon',
       'Duration_hours_suggested_friday_afternoon',
       'Duration_hours_required_monday_morning',
       'Duration_hours_required_tuesday_morning',
       'Duration_hours_required_wednesday_morning',
       'Duration_hours_required_thursday_morning',
       'Duration_hours_required_friday_morning',
       'Duration_hours_required_monday_afternoon',
       'Duration_hours_required_tuesday_afternoon',
       'Duration_hours_required_wednesday_afternoon',
       'Duration_hours_required_thursday_afternoon',
       'Duration_hours_required_friday_afternoon'], axis=1, inplace=True)

###########################################
# Sorting data to build the waiting lists : max durations first
# One waiting list per half day
###########################################

df_waiting_list['Priority_order_monday_morning'] = -1
df_waiting_list['Priority_order_tuesday_morning'] = -1
df_waiting_list['Priority_order_wednesday_morning'] = -1
df_waiting_list['Priority_order_thursday_morning'] = -1
df_waiting_list['Priority_order_friday_morning'] = -1

df_waiting_list['Priority_order_monday_afternoon'] = -1
df_waiting_list['Priority_order_tuesday_afternoon'] = -1
df_waiting_list['Priority_order_wednesday_afternoon'] = -1
df_waiting_list['Priority_order_thursday_afternoon'] = -1
df_waiting_list['Priority_order_friday_afternoon'] = -1


df_waiting_list.sort_values(by='Duration_hours_monday_morning', ascending=False, inplace=True, na_position='last')
df_waiting_list.reset_index(drop=True, inplace=True)
df_waiting_list['Priority_order_monday_morning'] = df_waiting_list.index

df_waiting_list.sort_values(by='Duration_hours_tuesday_morning', ascending=False, inplace=True, na_position='last')
df_waiting_list.reset_index(drop=True, inplace=True)
df_waiting_list['Priority_order_tuesday_morning'] = df_waiting_list.index

df_waiting_list.sort_values(by='Duration_hours_wednesday_morning', ascending=False, inplace=True, na_position='last')
df_waiting_list.reset_index(drop=True, inplace=True)
df_waiting_list['Priority_order_wednesday_morning'] = df_waiting_list.index

df_waiting_list.sort_values(by='Duration_hours_thursday_morning', ascending=False, inplace=True, na_position='last')
df_waiting_list.reset_index(drop=True, inplace=True)
df_waiting_list['Priority_order_thursday_morning'] = df_waiting_list.index

df_waiting_list.sort_values(by='Duration_hours_friday_morning', ascending=False, inplace=True, na_position='last')
df_waiting_list.reset_index(drop=True, inplace=True)
df_waiting_list['Priority_order_friday_morning'] = df_waiting_list.index



df_waiting_list.sort_values(by='Duration_hours_monday_afternoon', ascending=False, inplace=True, na_position='last')
df_waiting_list.reset_index(drop=True, inplace=True)
df_waiting_list['Priority_order_monday_afternoon'] = df_waiting_list.index

df_waiting_list.sort_values(by='Duration_hours_tuesday_afternoon', ascending=False, inplace=True, na_position='last')
df_waiting_list.reset_index(drop=True, inplace=True)
df_waiting_list['Priority_order_tuesday_afternoon'] = df_waiting_list.index

df_waiting_list.sort_values(by='Duration_hours_wednesday_afternoon', ascending=False, inplace=True, na_position='last')
df_waiting_list.reset_index(drop=True, inplace=True)
df_waiting_list['Priority_order_wednesday_afternoon'] = df_waiting_list.index

df_waiting_list.sort_values(by='Duration_hours_thursday_afternoon', ascending=False, inplace=True, na_position='last')
df_waiting_list.reset_index(drop=True, inplace=True)
df_waiting_list['Priority_order_thursday_afternoon'] = df_waiting_list.index

df_waiting_list.sort_values(by='Duration_hours_friday_afternoon', ascending=False, inplace=True, na_position='last')
df_waiting_list.reset_index(drop=True, inplace=True)
df_waiting_list['Priority_order_friday_afternoon'] = df_waiting_list.index


###########################################
# Exporting data : waiting list
###########################################

df_waiting_list.to_csv('./2_Waiting_lists.csv', index=False, index_label=True, header=True, encoding='utf-8', quotechar='"', decimal='.', sep=';')

