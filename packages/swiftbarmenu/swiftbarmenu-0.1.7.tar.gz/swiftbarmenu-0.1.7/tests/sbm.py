import sys

sys.path.append('.')

from src.swiftbarmenu import Menu, Notification


def main():
    m = Menu('Test')

    m.add_item('Item 1')

    m.add_image('tests/images/parrot.png', 'Parrot')

    item2 = m.add_item('Item 2', sep=True, checked=True)
    item2.add_item('Subitem 1')
    item2.add_item('Subitem 2')

    m.add_link('Item 3', 'https://example.com', color='yellow')

    m.add_item(':thermometer: Item 4', color='orange', sfcolor='black', sfsize=20)

    m.add_action('Notification...', ['show-notification'], sep=True)

    m.add_action_refresh(sep=True)

    m.dump()


def show_notification():
    Notification("Test notification", "This is a test Notification", "Click on the banner to open 'swiftbarmenu' GitHub repository", "https://github.com/sdelquin/swiftbarmenu").show()


if len(sys.argv) == 2 and sys.argv[1] == 'show-notification':
    show_notification()
else:
    main()
