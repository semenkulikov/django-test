from django import template
from treeMenu.models import MenuItem, Menu

register = template.Library()


@register.inclusion_tag('menu/draw_menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_path = request.path
    menu_items = MenuItem.objects.filter(menu__name=menu_name).select_related('parent')

    if not menu_items.exists():
        # Если элементы меню не найдены, возвращаем пустой контекст
        return {'menu_tree': None}

    def build_tree(items, parent=None):
        tree = []
        for item in items:
            if item.parent == parent:
                children = build_tree(items, item)
                tree.append({'item': item, 'children': children, 'active': False})
        return tree

    def mark_active(tree):
        """
        Устанавливает состояние активности и развернутости элементов меню.
        """

        def set_active(node):
            # Устанавливаем активность текущего узла
            node['active'] = current_path == node['item'].get_url()
            # Проверяем, активен ли хотя бы один дочерний узел
            has_active_children = any(set_active(child) for child in node['children'])
            # Если текущий узел активен или есть активные дочерние узлы
            if node['active'] or has_active_children:
                node['expanded'] = True
            else:
                node['expanded'] = False
            return node['active'] or has_active_children

        for node in tree:
            set_active(node)

    tree = build_tree(menu_items)
    mark_active(tree)
    return {'menu_tree': tree}


@register.simple_tag
def get_menus():
    return Menu.objects.all()
