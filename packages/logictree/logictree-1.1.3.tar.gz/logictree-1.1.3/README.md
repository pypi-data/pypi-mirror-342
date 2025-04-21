Install
============================================================
pip install logictree


Basic Use Case
============================================================
- import 
```python3
>>> from logictree import LogicTree, parse_logic_str
```

- create  
  include build a new Logic Tree object from a logic-string or logic-dict
```python3
>>> logic_dic = parse_logic_str('{0} and {1} and not {2} and not not {3}')
# logic_dic:
{'child_nodes': ['0',
                 '1',
                 {'child_nodes': ['2'], 'inverse': True, 'logic': None},
                 '3'],
'inverse': False,
'logic': 'and'}                       
>>> logic_tree = LogicTree.new_from_dict(logic_dic)
# logic_tree:
LogicTree(child_nodes=['0',
                       '1',
                       LogicTree(child_nodes=['2'], logic='and', inverse=True),
                       '3'],
          logic='and',
          inverse=False)
>>> logic_tree.to_str(line_feed=False)
'{0} and {1} and not {2} and {3}'
>>> logic_tree.to_str(line_feed=True)
'{0}\n'
'and {1}\n'
'and not {2}\n'
'and {3}'

>>> logic_tree = LogicTree.new_from_str('(({1} and {2} or {3}) and {4} or {5}) and {6} or {7} or {8} and ({9} or {10} and ({11} or {12} and {13}))')
>>> logic_tree.to_str(line_feed=False)
'(({1} and {2} or {3}) and {4} or {5}) and {6} or {7} or {8} and ({9} or {10} and ({11} or {12} and {13}))'
>>> logic_tree.to_str(line_feed=True)
'    (\n'
'            (\n'
'                    {1}\n'
'                    and {2}\n'
'                or {3}\n'
'            )\n'
'            and {4}\n'
'        or {5}\n'
'    )\n'
'    and {6}\n'
'or {7}\n'
'or \n'
'    {8}\n'
'    and (\n'
'        {9}\n'
'        or \n'
'            {10}\n'
'            and (\n'
'                {11}\n'
'                or \n'
'                    {12}\n'
'                    and {13}\n'
'            )\n'
'    )'
```

- simplify  
  include such as remove empty node, apply de-morgen, single node up
```python3
>>> logic_tree = LogicTree.new_from_str('not ({1} and ({2} or not {3}))')
>>> logic_tree.to_str_as_multi_lines()
'not (\n'
'{1}\n'
'and (\n'
'     {2}\n'
'     or not {3}\n'
'     )\n'
')'
>>> logic_tree.de_morgan(recursive=True).to_str_as_multi_lines()
'not {1}\n'
'or \n'
'    not {2}\n'
'    and {3}'  

>>> logic_tree = LogicTree(
        child_nodes=[
            # ((1))
            LogicTree(child_nodes=[LogicTree(child_nodes=['a11', ],
                                             logic='and',
                                             inverse=False)
                                   ],
                      logic='and',
                      inverse=False),
            # not ((1))
            LogicTree(child_nodes=[LogicTree(child_nodes=['aa11'],
                                             logic='and',
                                             inverse=False)
                                   ],
                      logic='and',
                      inverse=True),
            # ((not 1))
            LogicTree(child_nodes=[LogicTree(child_nodes=['b11', ],
                                             logic='and',
                                             inverse=True)
                                   ],
                      logic='and',
                      inverse=False),
            # not ((not 1))
            LogicTree(child_nodes=[LogicTree(child_nodes=['bb11'],
                                             logic='and',
                                             inverse=True)
                                   ],
                      logic='and',
                      inverse=True),
        ],
        logic='or',
        inverse=False)
>>> logic_tree.to_str_as_multi_lines()
'    {a11}\n'
'or \n'
'    not (\n'
'    {aa11}\n'
'    )\n'
'or \n'
'    not {b11}\n'
'or \n'
'    not (\n'
'    not {bb11}\n'
'    )'
>>> logic_tree.copy(recursive=True).simplify().to_str_as_multi_lines()
'{a11}\n'
'or not {aa11}\n'
'or not {b11}\n'
'or {bb11}' 
```

- modify  
  include such remove leaf nodes, merge with other
```python3
>>> s2 = '(({1} and {2} or {3}) and {1} or {2}) and {3} or {1} or {2} and ({3} or {1} and ({2} or {3} and {0}))'
>>> LogicTree.new_from_str(s2).collect_leaf_values()
{'0': 1, '1': 4, '2': 4, '3': 4}

>>> logic_tree = LogicTree.new_from_str('{1} and {2} and ({1} or {3})')
>>> logic_tree.remove_leaf_values({'1', '2'}).to_str_as_multi_lines()  
'{3}'

>>> logic_tree = LogicTree.new_from_str('{1} and {2}')                                     
>>> logic_tree.copy().merge_leaf_values('3', inverse=True, logic='or').to_str_as_one_line()
'{1} and {2} or not {3}'

>>> LogicTree.new_from_str('not ({1} or {2})').merge_leaf_values('3', '4', logic='or').to_str_as_one_line()
'not ({1} or {2} or not {3} or not {4})'

>>>  LogicTree.new_from_str('{1} or {2}').merge_other(LogicTree.new_from_str('{3} and {4}')).to_str_as_one_line()
'{3} and {4} and ({1} or {2})'

```

FAQ
============================================================
- follow-up plan?
  - depend