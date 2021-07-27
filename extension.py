import vscode
from youtubesearchpython import VideosSearch


ext = vscode.Extension(
        name='youtube', 
        display_name='Youtube', 
        version='1.0.2', 
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
        item = vscode.ext.QuickPickItem(result['title'],description=detail, link=result['link'])
        data.append(item)

    res = vscode.window.show_quick_pick(data)
    if not res:
        return
    vscode.env.open_external(res.link)

vscode.build(ext)