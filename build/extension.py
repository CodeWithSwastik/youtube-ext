# Built using vscode-ext

try:
    import vscode
except ModuleNotFoundError:
    import os
    os.system('pip3 install vscode-ext')
    import vscode

try:
    from youtubesearchpython import VideosSearch
except ModuleNotFoundError:
    import os
    os.system('pip3 install youtube-search-python')
    from youtubesearchpython import VideosSearch


ext = vscode.Extension(
        name='youtube', 
        display_name='Youtube', 
        version='1.0.1', 
        description='This extension lets you search for youtube videos.'
    )

ext.set_default_category(ext.display_name)

@ext.event
def on_activate():
    return 'Youtube has been activated'

@ext.command()
def search():
    options = vscode.ext.InputBoxOptions(title='What would you like to search for?')
    res = vscode.window.show_input_box(options)
    if not res:
        return
    data = []
    videosSearch = VideosSearch(res, limit = 10)
    results = videosSearch.result()['result']
    for result in results:
        channel = result['channel']['name']
        views = result['viewCount']['text']
        duration = result['duration']
        detail = f'Channel: {channel} | Views: {views} | Duration: {duration}'
        data.append({'label': result['title'], 'detail': detail, 'link': result['link']})

    res = vscode.window.show_quick_pick(data, {})
    if not res:
        return
    vscode.env.open_external(res['link'])



import sys
def ipc_main():
    globals()[sys.argv[1]]()

ipc_main()
