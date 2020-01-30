import dash
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import numpy as np
import pandas as pd
import datetime as dt
import pickle
from dash.dependencies import Input, Output, State

external_stylesheets = ['assets/1_style.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
app.config.suppress_callback_exceptions = True
app.title = 'Recommender System'

server = app.server

# Importing datasets
books = pd.read_csv('datasets/books_ml.csv')
ratings = pd.read_csv('datasets/ratings_ml.csv')

# Making another dataset
user_id = pd.DataFrame(ratings['user_id'].unique(), columns = ['user_id']).sort_values('user_id')

# Importing predictions
pred_title = pickle.load(open('predictions/predictions_title.sav', 'rb'))
pred_author = pickle.load(open('predictions/predictions_author.sav', 'rb'))
pred_tag = pickle.load(open('predictions/predictions_tag.sav', 'rb'))
pred_cf = pickle.load(open('predictions/predictions_cf.sav', 'rb'))

# Dashboard layout
app.layout = html.Div(children = [
    ## Top navigation bar
    dbc.Navbar(children = [ 
        dbc.Container(children = [
            dbc.Row(children = [
                dbc.Col(html.A(html.Img(src = 'assets/goodreads_1.png', height = '50rem'),
                    href = 'https://goodreads.com', target = '_blank')),
                dbc.Col(dbc.NavbarBrand('Recommender System',
                    style = {'font-size' : '1.375rem', 'font-weight' : 'bold'}, className = 'ml-2'))],
                align = 'center', no_gutters = True),
            dbc.Col(dbc.NavItem(id = 'live_time', style = {'padding-top' : '1rem',
                    'text-align' : 'right', 'list-style' : 'none'})),
                dcc.Interval(id = 'interval', interval = 1000, n_intervals = 0)])],
        fixed = 'top', sticky = 'top', color = 'rgb(240, 230, 140)', 
        style = {'height' : '5rem', 'border-bottom' : '0.125rem solid rgb(192, 192, 192)'}),
    ## Body
    html.Div(children = [
        ### Profile 
        html.Div(children = 
            html.A(html.Img(src = 'assets/goodreads_2.png', height = '60rem'),
                href = 'https://goodreads.com', target = '_blank'),
                style = {'margin-top' : '1.25rem'}),
            html.Div(children = 
                dcc.Markdown('''
                    The world's largest site for readers and book recommendations. **Goodreads** was founded 
                    in December 2006 by Otis Chandler and Elizabeth Khuri Chandler. It was officially launched 
                    in January 2007. In December 2007, the site had more than 650,000 registered users and over 
                    10 million books had been added. In March 2013, **Goodreads** was acquired by Amazon. 
                    In January 2020, according to the website, Goodreads had more than 90 million registered users 
                    and over 2.6 billion books had been added.'''), 
                    style = {'font-size' : '1.25rem', 'text-align' : 'justify', 
                            'margin-top' : '0.9375rem', 'margin-bottom' : '3rem'}),
        ### Recommendation section
        html.Div(children = 
            html.H1("Book's Recommendation"),
            style = {'border-bottom' : '0.1875rem solid black'}),
        html.Div(children =
            dcc.Markdown('''
                For the recommender system, We need **'user_id'** and **'book_id'** as reference 
                to start making recommendation. There are two tables provided below which list 
                all available users and books.'''),
                style = {'font-size' : '1.125rem', 'text-align' : 'justify', 
                        'margin-top' : '0.5rem', 'margin-bottom' : '2.5rem'}),
        ### DataTable
        html.Div(children =
            dbc.Row(children = [
                #### User table
                dbc.Col(id = 'table_1', children = [
                    html.P('User Table', style = {'font-weight' : 'bold', 'line-height' : '0.125rem'}),
                    dash_table.DataTable(
                        id = 'table_1_1', 
                        columns = [{'name' : 'User ID', 'id' : 'user_id'}],
                        style_header = {'background-color': 'rgb(189, 183, 107)', 'font-weight': 'bold'},
                        style_cell = {'text-align': 'center'},
                        data = user_id.to_dict('records'),
                        style_data = {'white-space': 'normal', 'height' : 'auto'},
                        page_action = 'native',
                        sort_action = 'native',
                        sort_mode = 'multi',
                        filter_action = 'native',
                        page_current = 0,
                        page_size = 10)], 
                    width = {'size' : 3}),
                #### Book table
                dbc.Col(id = 'table_2', children = [
                    html.P('Book Table', style = {'font-weight' : 'bold', 'line-height' : '0.125rem'}),
                    dash_table.DataTable(
                        id = 'table_2_1', 
                        columns = [{'name' : 'Book ID', 'id' : 'book_id'}, {'name' : 'Book Title', 'id' : 'title'}],
                        style_header = {'backgroundColor': 'rgb(189, 183, 107)', 'font-weight': 'bold'},
                        style_cell_conditional=[{'if': {'column_id': 'book_id'}, 
                                                        'width': '3rem', 'text-align' : 'center'},
                                                {'if': {'column_id': 'title'}, 
                                                        'width': '12rem', 'text-align' : 'left'}],
                        data = books[['book_id', 'title']].to_dict('records'),
                        style_data = {'white-space': 'normal', 'height' : 'auto'},
                        page_action = 'native',
                        sort_action = 'native',
                        sort_mode = 'multi',
                        filter_action = 'native',
                        page_current = 0,
                        page_size = 10)], 
                    width = {'size' : 6, 'offset' : 1})], 
                style = {'justify-content' : 'center'}, no_gutters = True)),
        ### Input data
        dbc.Row(children = 
            dbc.Col(children = [
                html.Div(html.H3('Input Data'), 
                    style = {'border-bottom' : '0.1rem solid black', 'margin-bottom' : '0.5rem'}),
                dbc.Form(children = [
                    #### Input User ID
                    dbc.FormGroup(children = [
                        dbc.Label('User ID:', width = 4, style = {'font-size' : '1.125rem'}),
                        dbc.Col(dbc.Input(id = 'input_user', type = 'number', min = 1, max = 53366, 
                                placeholder = 'Input a Number'), width = 8)],
                        style = {'margin-bottom' : '0.3rem'}, row = True),
                    #### Input Book ID
                    dbc.FormGroup(children = [
                        dbc.Label('Book ID:', width = 4, style = {'font-size' : '1.125rem'}),
                        dbc.Col(dbc.Input(id = 'input_book', type = 'number', min = 1, max = 1248,
                                placeholder = 'Input a Number'), width = 8)],
                        style = {'margin-bottom' : '0.3rem'}, row = True),
                    #### Input Content
                    dbc.FormGroup(children = [
                        dbc.Label('Content:', width = 4, style = {'font-size' : '1.125rem'}),
                        dbc.Col(dcc.Dropdown(id = 'input_content', 
                                    options = [
                                        {'label' : 'Title', 'value' : 1},
                                        {'label' : 'Author', 'value' : 2},
                                        {'label' : 'Tag', 'value' : 3}], 
                                    placeholder = 'Select a Feature',
                                    searchable = False,
                                    clearable= False))],
                        style = {'margin-bottom' : '0.3rem'}, row = True)]),
                    #### Recommend Button
                    html.Div(children = [
                        dbc.Button('Recommend!', id = 'recom'),
                        dbc.Toast(id = 'warning_1',
                            header = 'W A R N I N G ! ! !',                  
                            children = html.P('Please fill all required fields!', 
                                                style = {'font-size' : '1rem', 'text-align' : 'left'}, 
                                                className = 'mb-0'),
                            is_open = False, dismissable = True, duration = 3000, icon = 'danger',
                            style = {'position' : 'relative', 'top' : '0.5rem'}),
                        dbc.Modal(id = 'warning_2', children = [
                            dbc.ModalHeader('W A R N I N G ! ! !', 
                                style = {'background-color' : 'rgb(255, 0, 0, 0.8)'}),
                            dbc.ModalBody(id = 'modal_body'),
                            dbc.ModalFooter(dbc.Button('Close', id = 'close'))],
                            is_open = False, centered = True)],
                        style = {'text-align' : 'right'})], 
                width = {'size' : 4}), 
            justify = 'center', style = {'margin-top' : '1rem'}),
        ### Recommendation Output
        html.Div(id = 'output', style = {'margin-top' : '2rem'})],
        style = {'max-width' : '68.75rem', 'margin' : '0 auto'}),
    ## Bottom navigation bar
    dbc.Navbar(children = [
        dbc.Container(children = [
            html.H5('Created by Susanto'),
            dbc.Col(html.H5('© 2020'), style = {'text-align' : 'right'})])],
        color = 'rgb(240, 230, 140)', 
        style = {'border-top' : '0.125rem solid rgb(192, 192, 192)', 'height' : '4rem'})],
    style = {'background-color' : 'rgb(238, 232, 170, 0.5)'})

# Callback Live Time And Date
@app.callback(
    Output(component_id = 'live_time', component_property = 'children'),
    [Input(component_id = 'interval', component_property = 'n_intervals')])

def update_time(n):
    date_time = [
        html.P(dt.datetime.today().strftime('%A, %d %B %Y'), 
            style = {'line-height' : '0.67rem', 'font-size' : '1.25rem'}),
        html.P(dt.datetime.today().strftime('%H:%M:%S'), 
            style = {'line-height' : '0.67rem', 'font-size' : '1.25rem'})]
    return date_time

# Callback Recommendation
@app.callback(
    [Output(component_id = 'warning_1', component_property = 'is_open'),
    Output(component_id = 'warning_2', component_property = 'is_open'),
    Output(component_id = 'modal_body', component_property = 'children'),
    Output(component_id = 'output', component_property = 'children')],
    [Input(component_id = 'recom', component_property = 'n_clicks'),
    Input(component_id = 'close', component_property = 'n_clicks')],
    [State(component_id = 'warning_1', component_property = 'is_open'),
    State(component_id = 'warning_2', component_property = 'is_open'),
    State(component_id = 'input_user', component_property = 'value'),
    State(component_id = 'input_book', component_property = 'value'),
    State(component_id = 'input_content', component_property = 'value')])

def recommendation(n1, n2, open_toast, open_modal, user, book, content):
    output, modal_body  = '', ''
    try:
        ## Checking whether all fields have been filled or not
        user + book + content
        ## Recommendation Process
        if user not in ratings['user_id'].unique() and book not in ratings['book_id'].unique():
            modal_body = html.P('User ID and Book ID did not exist. Please check once more to the provided tables above.')
        elif user not in ratings['user_id'].unique():
            modal_body = html.P('User ID did not exist. Please check once more to the User ID table.')
        elif book not in ratings['book_id'].unique():
            modal_body = html.P('Book ID did not exist. Please check once more to the Book ID table.')
        else:
            open_modal = not open_modal
            if content == 1:
                content, pred = 'Title', pred_title
            elif content == 2:
                content, pred = 'Author', pred_author
            elif content == 3:
                content, pred = 'Tag', pred_tag

            ### Content-based Recommendation
            idx = books[books['book_id'] == book].index[0]
            recom = pd.Series(pred[idx]).sort_values(ascending = False)[1 : 11].index.to_list()

            rec_book = list()
            for i in [0, 5]:
                row = list()
                for j in range(1, 4): 
                    col = list()   
                    for iid, idx in zip(recom[i : i + 5], range(i, i + 5)):
                        if j == 1:
                            item = dbc.Col(html.Img(src = books.loc[iid]['image_url']), 
                                style = {'margin-bottom' : '0.25rem'})
                        elif j == 2:
                            item = dbc.Col(html.P(books.loc[iid]['title']))
                        else:
                            item = dbc.Col(children = [
                                dbc.Button('View Details', id = f'view_content_{idx + 1}', size = 'sm'),
                                dbc.Modal(id = f'modal_content_{idx + 1}', children = [
                                    dbc.ModalHeader(html.H3(f'Book #{idx + 1}'), style = {'background-color' : 'rgb(240, 230, 140)'}),
                                    dbc.ModalBody(children = [
                                        dbc.Row(children = [
                                            html.Div(html.Img(src = books.loc[iid]['image_url']),
                                                style = {'padding-top' : '0.3rem'}),
                                            dbc.Col(children = [
                                                dcc.Markdown(f'''**Book ID:** {iid}  
                                                **Title:** {books.loc[iid]['title']}  
                                                **Original Title:** {books.loc[iid]['original_title']}  
                                                **Author(s):** {books.loc[iid]['authors']}  
                                                **Original Publication Year:** {books.loc[iid]['original_publication_year']}  
                                                **Total Number of Edition(s):** {books.loc[iid]['books_count']}  
                                                **ISBN:** {books.loc[iid]['isbn']}  
                                                **ISBN13:** {books.loc[iid]['isbn13']}  
                                                **Language Code:** {books.loc[iid]['language_code']}  
                                                **Rating:** 
                                                {books.loc[iid]['average_rating']} ({books.loc[iid]['work_ratings_count']} ratings)  
                                                **Top-5 Tags:** {books.loc[iid]['top_5_tags']}''')],
                                                style = {'text-align' : 'justify'})])],  
                                    style = {'width' : '27rem', 'margin' : '0 auto'}),
                                    dbc.ModalFooter(dbc.Button('Close', id = f'close_content_{idx + 1}'))], 
                                is_open = False, centered = True)])
                        col.append(item)
                    col = dbc.Row(children = col, style = {'justify' : 'around'})
                    row.append(col)
                row = html.Div(children = row, style = {'margin-bottom' : '2rem'})
                rec_book.append(row)

            output_content = html.Div(children = [
                html.Div(html.H2(f'Top-10 Recommended Books Similar to Book with ID: {book} based on {content}'),
                    style = {'margin-bottom' : '0.5rem', 'border-bottom' : '0.15rem solid black'}),
                html.Div(children = rec_book)],
                style = {'margin-bottom' : '3rem'})

            ### CF-based Recommendation
            rec_book = list()
            for i in [0, 5]:
                row = list()
                for j in range(1, 4): 
                    col = list()   
                    for iid, idx in zip(pred_cf[user][i : i + 5], range(i, i + 5)):
                        if j == 1:
                            item = dbc.Col(html.Img(src = books[books['book_id'] == iid[0]]['image_url'].values[0]), 
                                style = {'margin-bottom' : '0.25rem'})
                        elif j == 2:
                            item = dbc.Col(html.P(books[books['book_id'] == iid[0]]['title'].values[0]))
                        else:
                            item = dbc.Col(children = [
                                dbc.Button('View Details', id = f'view_cf_{idx + 1}', size = 'sm'),
                                dbc.Modal(id = f'modal_cf_{idx + 1}', children = [
                                    dbc.ModalHeader(html.H3(f'Book #{idx + 1}'), 
                                        style = {'background-color' : 'rgb(240, 230, 140)'}),
                                    dbc.ModalBody(children = [
                                        dbc.Row(children = [
                                            html.Div(html.Img(src = books[books['book_id'] == iid[0]]['image_url'].values[0])),
                                            dbc.Col(children = [
                                                dcc.Markdown(f'''**Book ID:** {iid[0]}  
                                                **Title:** 
                                                {books[books['book_id'] == iid[0]]['title'].values[0]}  
                                                **Original Title:** 
                                                {books[books['book_id'] == iid[0]]['original_title'].values[0]}  
                                                **Author(s):** {books[books['book_id'] == iid[0]]['authors'].values[0]}  
                                                **Original Publication Year:** 
                                                {books[books['book_id'] == iid[0]]['original_publication_year'].values[0]}  
                                                **Total Number of Edition(s):** 
                                                {books[books['book_id'] == iid[0]]['books_count'].values[0]}  
                                                **ISBN:** {books[books['book_id'] == iid[0]]['isbn'].values[0]}  
                                                **ISBN13:** {books[books['book_id'] == iid[0]]['isbn13'].values[0]}  
                                                **Language Code:** {books[books['book_id'] == iid[0]]['language_code'].values[0]}  
                                                **Rating:** {books[books['book_id'] == iid[0]]['average_rating'].values[0]} 
                                                ({books[books['book_id'] == iid[0]]['work_ratings_count'].values[0]} ratings)  
                                                **Top-5 Tags:** {books[books['book_id'] == iid[0]]['top_5_tags'].values[0]}''')],
                                                style = {'text-align' : 'justify'})])],
                                    style = {'width' : '27rem', 'margin' : '0 auto'}),
                                    dbc.ModalFooter(dbc.Button('Close', id = f'close_cf_{idx + 1}'))],
                                    is_open = False, centered = True)])
                        col.append(item)
                    col = dbc.Row(children = col, style = {'justify' : 'around'})
                    row.append(col)
                row = html.Div(children = row, style = {'margin-bottom' : '2rem'})
                rec_book.append(row)

            output_cf = html.Div(children = [
                html.Div(html.H2(f'Top-10 Recommended Books for User with ID: {user}'),
                    style = {'margin-bottom' : '0.5rem', 'border-bottom' : '0.15rem solid black'}),
                html.Div(children = rec_book)],
                style = {'margin-bottom' : '3rem'})

            ### Combining the recommendation output
            output = [
                #### Chosen Book
                dbc.Row(dbc.Col(children = [
                    html.Div(html.H2('Your Book'), 
                        style = {'margin-bottom' : '0.5rem', 'border-bottom' : '0.15rem solid black'}),
                    dbc.Row(children = [
                        html.Div(html.Img(src = books[books['book_id'] == book]['image_url'].values[0]),
                            style = {'padding-top' : '0.3rem', 'margin-left' : '1rem'}),
                        dbc.Col(children = [
                            dcc.Markdown(f'''**Book ID:** {book}  
                            **Title:** 
                            {books[books['book_id'] == book]['title'].values[0]}  
                            **Original Title:** 
                            {books[books['book_id'] == book]['original_title'].values[0]}  
                            **Author(s):** {books[books['book_id'] == book]['authors'].values[0]}  
                            **Original Publication Year:** 
                            {books[books['book_id'] == book]['original_publication_year'].values[0]}  
                            **Total Number of Edition(s):** 
                            {books[books['book_id'] == book]['books_count'].values[0]}  
                            **ISBN:** {books[books['book_id'] == book]['isbn'].values[0]}  
                            **ISBN13:** {books[books['book_id'] == book]['isbn13'].values[0]}  
                            **Language Code:** {books[books['book_id'] == book]['language_code'].values[0]}  
                            **Rating:** {books[books['book_id'] == book]['average_rating'].values[0]} 
                            ({books[books['book_id'] == book]['work_ratings_count'].values[0]} ratings)  
                            **Top-5 Tags:** {books[books['book_id'] == book]['top_5_tags'].values[0]}''')],
                            style = {'text-align' : 'justify'})])], 
                    width = {'size' : 5}), 
                    style = {'margin-bottom' : '1rem'}),
                #### Content & CF-based recommendation
                output_content, output_cf]
        return False, not open_modal, modal_body, output
    except:
        ## This code runs when not all fields were filled
        if n1:
            return not open_toast, False, modal_body, output
        return open_toast, False, modal_body, output

# Callback for Details of Content-based Recommendation
for idx in range(1, 11):
    @app.callback(
    Output(component_id = f'modal_content_{idx}', component_property = 'is_open'),
    [Input(component_id = f'view_content_{idx}', component_property = 'n_clicks'),
    Input(component_id = f'close_content_{idx}', component_property = 'n_clicks')],
    [State(component_id = f'modal_content_{idx}', component_property = 'is_open')])

    def modal_content_open(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

# Callback for Details of CF-based Recommendation
for idx in range(1, 11):
    @app.callback(
    Output(component_id = f'modal_cf_{idx}', component_property = 'is_open'),
    [Input(component_id = f'view_cf_{idx}', component_property = 'n_clicks'),
    Input(component_id = f'close_cf_{idx}', component_property = 'n_clicks')],
    [State(component_id = f'modal_cf_{idx}', component_property = 'is_open')])

    def modal_cf_open(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

if __name__ == '__main__':
    app.run_server(debug=True)