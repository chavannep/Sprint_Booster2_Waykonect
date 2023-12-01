import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

###########################################
# Loading inputs : waiting and evse lists
###########################################

df_waiting_list = pd.read_csv('./2_Waiting_lists.csv', sep=';', encoding='utf-8', decimal='.')
df_evse = pd.read_csv('./3_EVSE_list.csv', sep=';', encoding='utf-8', decimal='.')


###########################################
# Checking Evse id : empty and duplicates
###########################################

empty_evse_idx = df_evse[df_evse['EVSE_Id'].isnull()].index
df_evse.drop(empty_evse_idx , inplace=True)
df_evse.reset_index(drop=True, inplace=True)

strict_duplicates = df_evse[df_evse.duplicated(subset=['EVSE_Id'], keep='first')].index
df_evse.drop(strict_duplicates , inplace=True)
df_evse.reset_index(drop=True, inplace=True)


###########################################
# Building Planer algo
###########################################

dict_planner = {'EVSE_Id':[], 'EVSE_Power':[], 'Vehicle_Id':[], 'Session_start_date':[], 'Session_end_date':[], 'User_confirm':[]}
df_planner = pd.DataFrame.from_dict(dict_planner)


planification_day = datetime.now()
planification_day_str = planification_day.strftime('%A')
week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

count = 1
# Looping through a moving week comprising 7 days
while(count<6):
    planification_day += pd.Timedelta(days=1)
    nextday_str = planification_day.strftime('%A')
    nextday_day = planification_day.day
    nextday_month = planification_day.month
    nextday_year = planification_day.year
    
    if(nextday_str=='Monday'):
        ############################
        # Monday morning 
        ############################
        # Looping through the waiting list for the considered half day
        cond = ( df_waiting_list['Availability_monday_morning'] == 1 )
        df_waiting_list_tmp = df_waiting_list[cond]
        df_waiting_list_tmp.sort_values(by='Priority_order_monday_morning', ascending=True, inplace=True)
        df_waiting_list_tmp.reset_index(drop=True, inplace=True)

        # Taking EVSE by high Power
        df_evse.sort_values(by='EVSE_Power', ascending=False, inplace=True, na_position='last')
        df_evse.reset_index(drop=True, inplace=True)

        # Building the planning for the considered half day
        for i in range(df_evse.shape[0]):
            if(i < df_waiting_list_tmp.shape[0]):
                dict_tmp = {'EVSE_Id':[], 'EVSE_Power':[], 'Vehicle_Id':[], 'Session_start_date':[], 'Session_end_date':[], 'User_confirm':[]}
                dict_tmp['EVSE_Id'] = [df_evse['EVSE_Id'].loc[i]]
                dict_tmp['EVSE_Power'] = [df_evse['EVSE_Power'].loc[i]]
                dict_tmp['Vehicle_Id'] = [df_waiting_list_tmp['Vehicle_Id'].loc[i]]
                dict_tmp['Session_start_date'] = [datetime(nextday_year,nextday_month,nextday_day,8,0,0).strftime('%d/%m/%Y %H:%M:%S')]
                dict_tmp['Session_end_date'] = [datetime(nextday_year,nextday_month,nextday_day,13,0,0).strftime('%d/%m/%Y %H:%M:%S')]
                # Session assumed automatically confirmed by user in this POC
                dict_tmp['User_confirm'] = [True]
                df_tmp = pd.DataFrame.from_dict(dict_tmp)
                df_planner = pd.concat([df_planner, df_tmp], join='outer', ignore_index=True)
                df_planner.reset_index(drop=True, inplace=True)

        ############################
        # Monday afternoon 
        ############################
        cond = ( df_waiting_list['Availability_monday_afternoon'] == 1 )
        df_waiting_list_tmp = df_waiting_list[cond]
        df_waiting_list_tmp.sort_values(by='Priority_order_monday_afternoon', ascending=True, inplace=True)
        df_waiting_list_tmp.reset_index(drop=True, inplace=True)

        df_evse.sort_values(by='EVSE_Power', ascending=False, inplace=True, na_position='last')
        df_evse.reset_index(drop=True, inplace=True)

        for i in range(df_evse.shape[0]):
            if(i < df_waiting_list_tmp.shape[0]):
                dict_tmp = {'EVSE_Id':[], 'EVSE_Power':[], 'Vehicle_Id':[], 'Session_start_date':[], 'Session_end_date':[], 'User_confirm':[]}
                dict_tmp['EVSE_Id'] = [df_evse['EVSE_Id'].loc[i]]
                dict_tmp['EVSE_Power'] = [df_evse['EVSE_Power'].loc[i]]
                dict_tmp['Vehicle_Id'] = [df_waiting_list_tmp['Vehicle_Id'].loc[i]]
                dict_tmp['Session_start_date'] = [datetime(nextday_year,nextday_month,nextday_day,13,0,0).strftime('%d/%m/%Y %H:%M:%S')]
                dict_tmp['Session_end_date'] = [datetime(nextday_year,nextday_month,nextday_day,18,0,0).strftime('%d/%m/%Y %H:%M:%S')]
                dict_tmp['User_confirm'] = [True]
                df_tmp = pd.DataFrame.from_dict(dict_tmp)
                df_planner = pd.concat([df_planner, df_tmp], join='outer', ignore_index=True)
                df_planner.reset_index(drop=True, inplace=True)
        # Next day
        count+=1


    
    elif(nextday_str=='Tuesday'):
        cond = ( df_waiting_list['Availability_tuesday_morning'] == 1 )
        df_waiting_list_tmp = df_waiting_list[cond]
        df_waiting_list_tmp.sort_values(by='Priority_order_tuesday_morning', ascending=True, inplace=True)
        df_waiting_list_tmp.reset_index(drop=True, inplace=True)

        df_evse.sort_values(by='EVSE_Power', ascending=False, inplace=True, na_position='last')
        df_evse.reset_index(drop=True, inplace=True)

        for i in range(df_evse.shape[0]):
            if(i < df_waiting_list_tmp.shape[0]):
                dict_tmp = {'EVSE_Id':[], 'EVSE_Power':[], 'Vehicle_Id':[], 'Session_start_date':[], 'Session_end_date':[], 'User_confirm':[]}
                dict_tmp['EVSE_Id'] = [df_evse['EVSE_Id'].loc[i]]
                dict_tmp['EVSE_Power'] = [df_evse['EVSE_Power'].loc[i]]
                dict_tmp['Vehicle_Id'] = [df_waiting_list_tmp['Vehicle_Id'].loc[i]]
                dict_tmp['Session_start_date'] = [datetime(nextday_year,nextday_month,nextday_day,8,0,0).strftime('%d/%m/%Y %H:%M:%S')]
                dict_tmp['Session_end_date'] = [datetime(nextday_year,nextday_month,nextday_day,13,0,0).strftime('%d/%m/%Y %H:%M:%S')]
                dict_tmp['User_confirm'] = [True]
                df_tmp = pd.DataFrame.from_dict(dict_tmp)
                df_planner = pd.concat([df_planner, df_tmp], join='outer', ignore_index=True)
                df_planner.reset_index(drop=True, inplace=True)

        
        cond = ( df_waiting_list['Availability_tuesday_afternoon'] == 1 )
        df_waiting_list_tmp = df_waiting_list[cond]
        df_waiting_list_tmp.sort_values(by='Priority_order_tuesday_afternoon', ascending=True, inplace=True)
        df_waiting_list_tmp.reset_index(drop=True, inplace=True)

        df_evse.sort_values(by='EVSE_Power', ascending=False, inplace=True, na_position='last')
        df_evse.reset_index(drop=True, inplace=True)

        for i in range(df_evse.shape[0]):
            if(i < df_waiting_list_tmp.shape[0]):
                dict_tmp = {'EVSE_Id':[], 'EVSE_Power':[], 'Vehicle_Id':[], 'Session_start_date':[], 'Session_end_date':[], 'User_confirm':[]}
                dict_tmp['EVSE_Id'] = [df_evse['EVSE_Id'].loc[i]]
                dict_tmp['EVSE_Power'] = [df_evse['EVSE_Power'].loc[i]]
                dict_tmp['Vehicle_Id'] = [df_waiting_list_tmp['Vehicle_Id'].loc[i]]
                dict_tmp['Session_start_date'] = [datetime(nextday_year,nextday_month,nextday_day,13,0,0).strftime('%d/%m/%Y %H:%M:%S')]
                dict_tmp['Session_end_date'] = [datetime(nextday_year,nextday_month,nextday_day,18,0,0).strftime('%d/%m/%Y %H:%M:%S')]
                dict_tmp['User_confirm'] = [True]
                df_tmp = pd.DataFrame.from_dict(dict_tmp)
                df_planner = pd.concat([df_planner, df_tmp], join='outer', ignore_index=True)
                df_planner.reset_index(drop=True, inplace=True)
        # Next day
        count+=1


    
    elif(nextday_str=='Wednesday'):
        cond = ( df_waiting_list['Availability_wednesday_morning'] == 1 )
        df_waiting_list_tmp = df_waiting_list[cond]
        df_waiting_list_tmp.sort_values(by='Priority_order_wednesday_morning', ascending=True, inplace=True)
        df_waiting_list_tmp.reset_index(drop=True, inplace=True)

        df_evse.sort_values(by='EVSE_Power', ascending=False, inplace=True, na_position='last')
        df_evse.reset_index(drop=True, inplace=True)

        for i in range(df_evse.shape[0]):
            if(i < df_waiting_list_tmp.shape[0]):
                dict_tmp = {'EVSE_Id':[], 'EVSE_Power':[], 'Vehicle_Id':[], 'Session_start_date':[], 'Session_end_date':[], 'User_confirm':[]}
                dict_tmp['EVSE_Id'] = [df_evse['EVSE_Id'].loc[i]]
                dict_tmp['EVSE_Power'] = [df_evse['EVSE_Power'].loc[i]]
                dict_tmp['Vehicle_Id'] = [df_waiting_list_tmp['Vehicle_Id'].loc[i]]
                dict_tmp['Session_start_date'] = [datetime(nextday_year,nextday_month,nextday_day,8,0,0).strftime('%d/%m/%Y %H:%M:%S')]
                dict_tmp['Session_end_date'] = [datetime(nextday_year,nextday_month,nextday_day,13,0,0).strftime('%d/%m/%Y %H:%M:%S')]
                dict_tmp['User_confirm'] = [True]
                df_tmp = pd.DataFrame.from_dict(dict_tmp)
                df_planner = pd.concat([df_planner, df_tmp], join='outer', ignore_index=True)
                df_planner.reset_index(drop=True, inplace=True)

        
        cond = ( df_waiting_list['Availability_wednesday_afternoon'] == 1 )
        df_waiting_list_tmp = df_waiting_list[cond]
        df_waiting_list_tmp.sort_values(by='Priority_order_wednesday_afternoon', ascending=True, inplace=True)
        df_waiting_list_tmp.reset_index(drop=True, inplace=True)

        df_evse.sort_values(by='EVSE_Power', ascending=False, inplace=True, na_position='last')
        df_evse.reset_index(drop=True, inplace=True)

        for i in range(df_evse.shape[0]):
            if(i < df_waiting_list_tmp.shape[0]):
                dict_tmp = {'EVSE_Id':[], 'EVSE_Power':[], 'Vehicle_Id':[], 'Session_start_date':[], 'Session_end_date':[], 'User_confirm':[]}
                dict_tmp['EVSE_Id'] = [df_evse['EVSE_Id'].loc[i]]
                dict_tmp['EVSE_Power'] = [df_evse['EVSE_Power'].loc[i]]
                dict_tmp['Vehicle_Id'] = [df_waiting_list_tmp['Vehicle_Id'].loc[i]]
                dict_tmp['Session_start_date'] = [datetime(nextday_year,nextday_month,nextday_day,13,0,0).strftime('%d/%m/%Y %H:%M:%S')]
                dict_tmp['Session_end_date'] = [datetime(nextday_year,nextday_month,nextday_day,18,0,0).strftime('%d/%m/%Y %H:%M:%S')]
                dict_tmp['User_confirm'] = [True]
                df_tmp = pd.DataFrame.from_dict(dict_tmp)
                df_planner = pd.concat([df_planner, df_tmp], join='outer', ignore_index=True)
                df_planner.reset_index(drop=True, inplace=True)
        # Next day
        count+=1


    elif(nextday_str=='Thursday'):
        cond = ( df_waiting_list['Availability_thursday_morning'] == 1 )
        df_waiting_list_tmp = df_waiting_list[cond]
        df_waiting_list_tmp.sort_values(by='Priority_order_thursday_morning', ascending=True, inplace=True)
        df_waiting_list_tmp.reset_index(drop=True, inplace=True)

        df_evse.sort_values(by='EVSE_Power', ascending=False, inplace=True, na_position='last')
        df_evse.reset_index(drop=True, inplace=True)

        for i in range(df_evse.shape[0]):
            if(i < df_waiting_list_tmp.shape[0]):
                dict_tmp = {'EVSE_Id':[], 'EVSE_Power':[], 'Vehicle_Id':[], 'Session_start_date':[], 'Session_end_date':[], 'User_confirm':[]}
                dict_tmp['EVSE_Id'] = [df_evse['EVSE_Id'].loc[i]]
                dict_tmp['EVSE_Power'] = [df_evse['EVSE_Power'].loc[i]]
                dict_tmp['Vehicle_Id'] = [df_waiting_list_tmp['Vehicle_Id'].loc[i]]
                dict_tmp['Session_start_date'] = [datetime(nextday_year,nextday_month,nextday_day,8,0,0).strftime('%d/%m/%Y %H:%M:%S')]
                dict_tmp['Session_end_date'] = [datetime(nextday_year,nextday_month,nextday_day,13,0,0).strftime('%d/%m/%Y %H:%M:%S')]
                dict_tmp['User_confirm'] = [True]
                df_tmp = pd.DataFrame.from_dict(dict_tmp)
                df_planner = pd.concat([df_planner, df_tmp], join='outer', ignore_index=True)
                df_planner.reset_index(drop=True, inplace=True)

        
        cond = ( df_waiting_list['Availability_thursday_afternoon'] == 1 )
        df_waiting_list_tmp = df_waiting_list[cond]
        df_waiting_list_tmp.sort_values(by='Priority_order_thursday_afternoon', ascending=True, inplace=True)
        df_waiting_list_tmp.reset_index(drop=True, inplace=True)

        df_evse.sort_values(by='EVSE_Power', ascending=False, inplace=True, na_position='last')
        df_evse.reset_index(drop=True, inplace=True)

        for i in range(df_evse.shape[0]):
            if(i < df_waiting_list_tmp.shape[0]):
                dict_tmp = {'EVSE_Id':[], 'EVSE_Power':[], 'Vehicle_Id':[], 'Session_start_date':[], 'Session_end_date':[], 'User_confirm':[]}
                dict_tmp['EVSE_Id'] = [df_evse['EVSE_Id'].loc[i]]
                dict_tmp['EVSE_Power'] = [df_evse['EVSE_Power'].loc[i]]
                dict_tmp['Vehicle_Id'] = [df_waiting_list_tmp['Vehicle_Id'].loc[i]]
                dict_tmp['Session_start_date'] = [datetime(nextday_year,nextday_month,nextday_day,13,0,0).strftime('%d/%m/%Y %H:%M:%S')]
                dict_tmp['Session_end_date'] = [datetime(nextday_year,nextday_month,nextday_day,18,0,0).strftime('%d/%m/%Y %H:%M:%S')]
                dict_tmp['User_confirm'] = [True]
                df_tmp = pd.DataFrame.from_dict(dict_tmp)
                df_planner = pd.concat([df_planner, df_tmp], join='outer', ignore_index=True)
                df_planner.reset_index(drop=True, inplace=True)
        # Next day
        count+=1


    elif(nextday_str=='Friday'):
        cond = ( df_waiting_list['Availability_friday_morning'] == 1 )
        df_waiting_list_tmp = df_waiting_list[cond]
        df_waiting_list_tmp.sort_values(by='Priority_order_friday_morning', ascending=True, inplace=True)
        df_waiting_list_tmp.reset_index(drop=True, inplace=True)

        df_evse.sort_values(by='EVSE_Power', ascending=False, inplace=True, na_position='last')
        df_evse.reset_index(drop=True, inplace=True)

        for i in range(df_evse.shape[0]):
            if(i < df_waiting_list_tmp.shape[0]):
                dict_tmp = {'EVSE_Id':[], 'EVSE_Power':[], 'Vehicle_Id':[], 'Session_start_date':[], 'Session_end_date':[], 'User_confirm':[]}
                dict_tmp['EVSE_Id'] = [df_evse['EVSE_Id'].loc[i]]
                dict_tmp['EVSE_Power'] = [df_evse['EVSE_Power'].loc[i]]
                dict_tmp['Vehicle_Id'] = [df_waiting_list_tmp['Vehicle_Id'].loc[i]]
                dict_tmp['Session_start_date'] = [datetime(nextday_year,nextday_month,nextday_day,8,0,0).strftime('%d/%m/%Y %H:%M:%S')]
                dict_tmp['Session_end_date'] = [datetime(nextday_year,nextday_month,nextday_day,13,0,0).strftime('%d/%m/%Y %H:%M:%S')]
                dict_tmp['User_confirm'] = [True]
                df_tmp = pd.DataFrame.from_dict(dict_tmp)
                df_planner = pd.concat([df_planner, df_tmp], join='outer', ignore_index=True)
                df_planner.reset_index(drop=True, inplace=True)

        
        cond = ( df_waiting_list['Availability_friday_afternoon'] == 1 )
        df_waiting_list_tmp = df_waiting_list[cond]
        df_waiting_list_tmp.sort_values(by='Priority_order_friday_afternoon', ascending=True, inplace=True)
        df_waiting_list_tmp.reset_index(drop=True, inplace=True)

        df_evse.sort_values(by='EVSE_Power', ascending=False, inplace=True, na_position='last')
        df_evse.reset_index(drop=True, inplace=True)

        for i in range(df_evse.shape[0]):
            if(i < df_waiting_list_tmp.shape[0]):
                dict_tmp = {'EVSE_Id':[], 'EVSE_Power':[], 'Vehicle_Id':[], 'Session_start_date':[], 'Session_end_date':[], 'User_confirm':[]}
                dict_tmp['EVSE_Id'] = [df_evse['EVSE_Id'].loc[i]]
                dict_tmp['EVSE_Power'] = [df_evse['EVSE_Power'].loc[i]]
                dict_tmp['Vehicle_Id'] = [df_waiting_list_tmp['Vehicle_Id'].loc[i]]
                dict_tmp['Session_start_date'] = [datetime(nextday_year,nextday_month,nextday_day,13,0,0).strftime('%d/%m/%Y %H:%M:%S')]
                dict_tmp['Session_end_date'] = [datetime(nextday_year,nextday_month,nextday_day,18,0,0).strftime('%d/%m/%Y %H:%M:%S')]
                dict_tmp['User_confirm'] = [True]
                df_tmp = pd.DataFrame.from_dict(dict_tmp)
                df_planner = pd.concat([df_planner, df_tmp], join='outer', ignore_index=True)
                df_planner.reset_index(drop=True, inplace=True)
        # Next day
        count+=1
        
###########################################
# Exporting data : calendar on next 7 days for all EVSE and users slected after waiting list
########################################### 

df_planner.sort_values(by=['Session_start_date','EVSE_Id'], ascending=[True,True], inplace=True)
df_planner.reset_index(drop=True, inplace=True)

df_planner.to_csv('./5_Planning_week_ahead.csv', index=False, index_label=True, header=True, encoding='utf-8', quotechar='"', decimal='.', sep=';')
