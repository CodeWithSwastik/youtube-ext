# Built using vscode-ext

import sys
import vscode
from youtubesearchpython import VideosSearch


ext = vscode.Extension(
        name='youtube', 
        display_name='Youtube', 
        version='1.1.2', 
        description='This extension lets you search for youtube videos.'
    )

ext.set_default_category(ext.display_name)

@ext.event
def on_activate():
    return 'Youtube has been activated'

@ext.command(keybind='CTRL+F9')
def search():
    editor = vscode.window.ActiveTextEditor()
    if not editor or editor.selection.is_empty:
        options = vscode.ext.InputBoxOptions(title='What would you like to search for?')
        res = vscode.window.show_input_box(options)
    else:
        doc = editor.document
        res = f'{doc.get_text(editor.selection)} + {doc.language_id}'

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
        item = vscode.QuickPickItem(result['title'],detail, link=result['link'])
        data.append(item)
    if len(data) == 0:
        return vscode.show_info_message(f'No videos found for the search term: {res}')
    res = vscode.window.show_quick_pick(data)
    if not res:
        return
    vscode.env.open_external(res.link)



def ipc_main():
    globals()[sys.argv[1]]()

ipc_main()
