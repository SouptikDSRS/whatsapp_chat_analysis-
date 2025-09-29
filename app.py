import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import pandas as pd

st.sidebar.title("WhatsApp chat Analyser")

upload_file = st.sidebar.file_uploader("Choose a file")

if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        num_message, words, num_media_messages, num_link = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_message)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Shared Media")
            st.title(num_media_messages)

        with col4:
            st.header("Total Shared links")
            st.title(num_link)

        if selected_user == 'Overall':
            st.title('Most busy User')
            x,new_df = helper.graph_user(df) 

            fig, ax = plt.subplots()
            ax.bar(x.index, x.values,color = 'red')
            plt.xticks(rotation=90)

            col1, col2 = st.columns(2)
            with col1:
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)
    st.title('Message vs Months')
    col1,col2 = st.columns(2)
    month_df = helper.message_timeline(selected_user,df)
    with col1:
        fig,ax = plt.subplots()
        ax.plot(month_df['time'],month_df['message'],color = 'green')
        plt.xticks(rotation = 'vertical')    
        st.pyplot(fig)
    with col2:
        st.dataframe(month_df)


    st.title('Message vs Daily')
    col1,col2 = st.columns(2)
    daily_df = helper.daily_timeline(selected_user,df)
    with col1:
        fig,ax = plt.subplots()
        ax.plot(daily_df['only_date'],daily_df['message'],color = 'green')
        plt.xticks(rotation = 'vertical')    
        st.pyplot(fig)
    with col2:
        st.dataframe(daily_df)


## activity map
    st.title('Activity  Map')
    col1,col2 = st.columns(2)
    with col1:
        st.header("Most Busy Day")
        daily_num = helper.week_activity_map(selected_user,df)  
        fig,ax = plt.subplots()
        ax.bar(daily_num.index,daily_num.values) 
        plt.xticks(rotation = 'vertical')  
        st.pyplot(fig)
    with col2:
        st.header("Most busy Month")
        month_num = helper.month_activity_map(selected_user,df)  
        fig,ax = plt.subplots()
        ax.bar(month_num.index,month_num.values,color='orange')   
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)



    #wordcloud
    st.title('Word Cloud')
    df_wc = helper.create_word_cloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

    #Most Common Words
    st.title('Most Common Used Words')
    most_common_df = helper.most_common_words(selected_user,df)
    fig , ax = plt.subplots()
    ax.barh(most_common_df[0],most_common_df[1])
    plt.xticks(rotation = 'vertical')

    st.pyplot(fig)
    st.title('Emoji Checker')
    emoji_df = helper.emoji_helper(selected_user, df)

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df)  # shows actual emojis in the table

    with col2:
        fig, ax = plt.subplots()
        ax.pie(emoji_df[1].head(), labels=emoji_df[1].head().index, autopct="%0.2f%%")
        st.pyplot(fig)

    




