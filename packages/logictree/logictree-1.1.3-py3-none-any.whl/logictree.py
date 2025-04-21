# -*- coding:utf-8  -*-
import collections
import dataclasses
from typing import Literal, Tuple, List, Dict, Set, Optional, Union


def parse_logic_str(logic_str: str, /) -> dict:
    """解析逻辑字符串

    :param logic_str: 如   '{1} or not ({2} and {3} or {4}) and {5}'
    :return: dict, 如：
         {'child_nodes': ['1',
                          {'child_nodes': [{'child_nodes': [{'child_nodes': ['2', '3'],
                                                             'inverse': False,
                                                             'logic': 'and'},
                                                            '4'],
                                            'inverse': True,
                                            'logic': 'or'},
                                           '5'],
                           'logic': 'and'}],
          'inverse': False,
          'logic': 'or'}
    """
    remain_part: str = logic_str.lower().lstrip()
    if not remain_part:
        return {'child_nodes': []}
    # 用于标记 not，有可能多个 not 连着，如 not not not {1}
    flag_not = False
    # 是否存入最近的 and 节点
    into_latest_and_node = False
    cu_pos = len(logic_str) - len(remain_part)
    parent_nodes_stack = []
    state_stack = ['waiting_new_unit']
    current_node = {'child_nodes': [], 'inverse': False, 'logic': None}
    while remain_part:
        # state 可能是 { ( not and or ''  '' 代表起始状态
        state = state_stack[-1]
        if state == 'waiting_new_unit':
            # 等待新的单元
            #  {1} 或者 ( ... 或者 not ... 或者 not (
            if remain_part[0] == '{':
                # 新增一个叶子节点
                index, j = _lookup_index(remain_part, cu_pos)
                # 叶子节点不需要记录其 parent
                current_node['child_nodes'].append(index)
                remain_part_new = remain_part[j + 1:].lstrip()
                cu_pos += len(remain_part) - len(remain_part_new)
                remain_part = remain_part_new
                state_stack[-1] = 'after_index'
            elif remain_part[0] == '(':
                # 出现左端圆括号时，新建一个非叶子节点，并切换到新节点
                new_node = {'child_nodes': [], 'logic': None, 'inverse': False}
                current_node['child_nodes'].append(new_node)
                parent_nodes_stack.append(current_node)
                current_node = new_node
                remain_part_new = remain_part[1:].lstrip()
                cu_pos += len(remain_part) - len(remain_part_new)
                remain_part = remain_part_new
                state_stack.append('waiting_new_unit')
            elif remain_part[: 3] == 'not':
                flag_not = True
                remain_part_new = remain_part[3:].lstrip()
                cu_pos += len(remain_part) - len(remain_part_new)
                remain_part = remain_part_new
                state_stack[-1] = 'after_and_or_not'
            else:
                raise ValueError('Unexpected sub-string at position %s: %s' % (cu_pos, remain_part))
        elif state == 'after_index':
            # 前一个是{1}，那么后面允许未：{1} and, {1} or, {1})
            if remain_part[: 3] == 'and':
                if current_node['logic'] is None:
                    current_node['logic'] = 'and'  # noqa
                elif current_node['logic'] == 'or':
                    """例如 {1} or {2} and {N} and {N+1}
                    current_node: 
                    {'logic': 'or', 'child_nodes': [1, 2, ]}
                    -> 
                    {'logic': 'or', 'child_nodes': [1, 
                                                    {'logic': 'and', 'child_nodes':  [2, {'index': N}, ]}
                                                    ]
                    }                    
                    """
                    latest_child_node: dict = current_node['child_nodes'][-1]
                    if (not isinstance(latest_child_node, dict)
                            or latest_child_node['logic'] == 'or'
                            or latest_child_node['inverse']):
                        """如果最近的节点是叶子节点，或者 是 or 节点，或者 inverse=True
                            a or b and cu  ->  a or (b and cu)          
                            a or (b or (b2 and b3)) and cu  ->  a or ((b or (b2 and b3)) and cu)
                            a or not (b ...) and cu  ->  a or (not (b ...) and cu)      
                        否则，是非叶子节点，且是 and                            
                            a or (b and b2 and cu)  ->  a or (b and b2 and cu)
                        """
                        new_node = {'logic': 'and',
                                    'child_nodes': [latest_child_node, ],
                                    'inverse': False}
                        current_node['child_nodes'][-1] = new_node
                    elif latest_child_node['logic'] is None:
                        # a or (b and cu)
                        latest_child_node['logic'] = 'and'
                    into_latest_and_node = True
                remain_part_new = remain_part[3:].lstrip()
                cu_pos += len(remain_part) - len(remain_part_new)
                remain_part = remain_part_new
                state_stack[-1] = 'after_and_or_not'
            elif remain_part[: 2] == 'or':
                if current_node['logic'] is None:
                    current_node['logic'] = 'or'  # noqa
                elif current_node['logic'] == 'and':
                    """例如 {1} and {2} or {N}
                    current_node: 
                    {'logic': 'and', 'child_nodes': [1, 2, ]}
                    -> 
                    {'logic': 'or', 'child_nodes': [{'logic': 'and', 
                                                     'child_nodes': [1, 2],}, 
                                                    {'index': N},
                                                    ]
                    }
                    如果父节点是 and 呢？and not ({1} and {2} or {N})
                    结论：改变当前节点，而不是修改父节点
                    进一步地：
                    {1} and {2} or {N} or {K}
                    {1} and {2} or {N} and {K}
                    """
                    current_node_copy = current_node.copy()
                    current_node['logic'] = 'or'  # noqa
                    current_node['child_nodes'] = [current_node_copy]
                    current_node_copy['inverse'] = False
                remain_part_new = remain_part[2:].lstrip()
                cu_pos += len(remain_part) - len(remain_part_new)
                remain_part = remain_part_new
                state_stack[-1] = 'after_and_or_not'
            elif remain_part[: 1] == ')':
                if len(state_stack) == 1:
                    # 如果遇到 ...)  且 ... 部分无 (
                    raise ValueError('Unexpected sub-string at position %s: %s' % (cu_pos, remain_part))
                # 如 ... {1}) 此时返回父节点
                parent_node = parent_nodes_stack.pop()
                if len(current_node['child_nodes']) == 1:
                    node_unique: dict = current_node['child_nodes'][0]
                    # 如果 current_node 中只有 1 个子节点，将该子节点提上来
                    if current_node['inverse']:
                        # not (cu) -> not cu
                        if isinstance(node_unique, dict):
                            if node_unique['inverse'] and len(node_unique['child_nodes']) == 1:
                                # not (not x) -> x
                                node_unique = node_unique['child_nodes'][0]
                            else:
                                node_unique['inverse'] = not node_unique['inverse']
                        else:
                            node_unique = {'child_nodes': [node_unique], 'inverse': True, 'logic': None}
                    parent_latest_child_node: dict = parent_node['child_nodes'][-1]
                    if parent_latest_child_node['logic'] == 'and':
                        """当 parent 中最近一个子节点是 and 节点 时，node_unique 必定是该 and 节点的最后一个子节点
                        a and (cu)  或者  a or (b and (cu))
                        a or (cu)   或者  a and (b or (cu))
                        """
                        parent_latest_child_node['child_nodes'][-1] = node_unique
                    else:
                        # node_unique 是 parent_node 中最后一个子节点，
                        parent_node['child_nodes'][-1] = node_unique
                current_node = parent_node
                remain_part_new = remain_part[1:].lstrip()
                cu_pos += len(remain_part) - len(remain_part_new)
                remain_part = remain_part_new
                state_stack.pop(-1)
                if state_stack:
                    state_stack[-1] = 'after_index'
            else:
                raise ValueError('Unexpected sub-string at position %s: %s' % (cu_pos, remain_part))
        elif state == 'after_and_or_not':
            # not {1} 或者 not ( 或者 not not
            # and {1} 或者 and ( 或者 and not
            # or {1} 或者 or ( 或者 or not
            if remain_part[0] == '{':
                index, j = _lookup_index(remain_part, cu_pos)
                if flag_not:
                    new_node = {'child_nodes': [index], 'inverse': True, 'logic': None}
                    flag_not = False
                else:
                    new_node = index
                # {1} or {2} and {N} 或者  {1} or {2} or {N}
                # 存入 sub-and 节点  存入本节点
                # {1} and {2} or {N} 或者  {1} and {2} and {N}
                # 存入本节点 存入本节点
                if into_latest_and_node:
                    current_node['child_nodes'][-1]['child_nodes'].append(new_node)  # noqa
                    into_latest_and_node = False
                else:
                    current_node['child_nodes'].append(new_node)
                remain_part_new = remain_part[j + 1:].lstrip()
                cu_pos += len(remain_part) - len(remain_part_new)
                remain_part = remain_part_new
                state_stack[-1] = 'after_index'
            elif remain_part[0] == '(':
                new_node = {'child_nodes': [], 'logic': None, 'inverse': flag_not}
                flag_not = False
                if into_latest_and_node:
                    current_node['child_nodes'][-1]['child_nodes'].append(new_node)  # noqa
                    into_latest_and_node = False
                else:
                    current_node['child_nodes'].append(new_node)
                parent_nodes_stack.append(current_node)
                current_node = new_node
                remain_part_new = remain_part[1:].lstrip()
                cu_pos += len(remain_part) - len(remain_part_new)
                remain_part = remain_part_new
                state_stack.append('waiting_new_unit')
            elif remain_part[: 3] == 'not':
                # 出现 not 时，是否叶子节点是不确定的
                flag_not = not flag_not
                remain_part_new = remain_part[3:].lstrip()
                cu_pos += len(remain_part) - len(remain_part_new)
                remain_part = remain_part_new
                state_stack[-1] = 'after_and_or_not'
            else:
                raise ValueError('Unexpected sub-string at position %s: %s' % (cu_pos, remain_part))
    if state_stack and state_stack != ['after_index']:
        raise ValueError("until the end of the string, cannot found equal number of ) related to (")
    if len(current_node['child_nodes']) == 1 and isinstance(current_node['child_nodes'][0], dict):
        current_node = current_node['child_nodes'][0]
    return current_node


def _lookup_index(remain_part: str, cu_pos: int, /) -> Tuple[str, int]:
    j = remain_part.find('}')
    if j == -1:
        raise ValueError('{ at position %s cannot find related }' % (cu_pos,))
    if j == 0:
        raise ValueError('logic index at position %s is empty' % (cu_pos,))
    return remain_part[1:j], j


class PlaceHolder(object):
    def __init__(self, black_list: Set[str], /, *, holder_prefix: str = 'holder'):
        self.black_list = black_list
        self.holder_prefix = holder_prefix
        self.holder_index = -1

    def get_new_holder(self) -> str:
        """

        :return:
        """
        self.holder_index += 1
        while self.holder_prefix + '_' + str(self.holder_index) in self.black_list:
            self.holder_index += 1
        return self.holder_prefix + '_' + str(self.holder_index)


@dataclasses.dataclass()
class LogicTree(object):
    """逻辑树
    """
    need_enclosed = {'or'}
    # 该节点所包括的子节点, str 时为叶子值，否则是个子逻辑树
    child_nodes: List[Union[str, 'LogicTree']] = dataclasses.field(default_factory=list)
    # 全部节点之间 是 and 还是 or
    logic: Optional[Literal['or', 'and']] = 'and'
    # 是否取反, 如 not (child_1 and child_2 ...)
    inverse: bool = False

    def remove_leaf_values(self, leaf_values: Set[str], /):
        """按叶子值移除特定若干叶子节点

        :param leaf_values:
        :return:
        """
        if not leaf_values:
            return
        node_que = collections.deque([self])
        while node_que:
            node = node_que.popleft()
            remain_child_nodes = []
            for ch in node.child_nodes:
                if isinstance(ch, LogicTree):
                    remain_child_nodes.append(ch)
                    # 保留，但需要进一步处理
                    node_que.append(ch)
                elif ch not in leaf_values:
                    remain_child_nodes.append(ch)
            node.child_nodes = remain_child_nodes
        self.simplify()
        return self

    def collect_leaf_values(self) -> Dict[str, int]:
        """汇集全部叶子节点的索引

        :return: dict of index:出现次数
        """
        tmp = collections.Counter()
        que = collections.deque([self])
        while que:
            node = que.popleft()
            for ch in node.child_nodes:
                if isinstance(ch, LogicTree):
                    que.append(ch)
                else:
                    tmp.update([ch])
        return tmp

    def copy(self, *, recursive: bool = False, ):
        """

        :param recursive: 缺省为 False 时为 浅拷贝， True 时相当于 deepcopy
        :return:
        """
        if not recursive:
            return LogicTree(child_nodes=self.child_nodes.copy(),
                             logic=self.logic, inverse=self.inverse)
        return LogicTree(child_nodes=[ch.copy(recursive=True) if isinstance(ch, LogicTree) else ch
                                      for ch in self.child_nodes],
                         logic=self.logic, inverse=self.inverse)

    def is_leaf_node(self) -> bool:
        """是否叶子节点

        :return:
        """
        return len(self.child_nodes) == 1 and not isinstance(self.child_nodes[0], LogicTree)

    def de_morgan(self, *, recursive: bool = False, ) -> 'LogicTree':
        """使用德摩根定律，去掉节点的 not
        not (A and B)   == not A or not B
        not (A or B)    == not A and not B

        :param recursive: 
        :return: 
        """
        if self.inverse:
            if self.is_leaf_node():
                # {'child_nodes': ['1'], 'inverse': True, } 这种情况不去 not
                return self
            new_child_nodes = []
            for ch in self.child_nodes:
                if isinstance(ch, LogicTree):
                    ch.inverse = not ch.inverse
                    if not ch.inverse and ch.is_leaf_node():
                        # {'child_nodes': ['1'], 'inverse': False, } 变换为 1
                        ch = ch.child_nodes[0]
                else:
                    ch = LogicTree([ch], inverse=True)
                new_child_nodes.append(ch)
            self.child_nodes = new_child_nodes
            if self.logic == 'and':
                # not (A and B)
                self.logic = 'or'
            else:
                # not (A or B)
                self.logic = 'and'
            self.inverse = False
        if recursive:
            for ch in self.child_nodes:
                if isinstance(ch, LogicTree):
                    ch.de_morgan(recursive=True)
        return self

    def simplify(self, *, de_morgan: bool = False) -> 'LogicTree':
        """简化
        1.移除空节点
            空节点只会发生在叶子节点上，且可能会向上传播
            如 [[], []]
        2.子节点上移展开到父节点
            (... and (1 and 2) and ...)                 -> (... and 1 and 2 and ...)
            (... and (1 or 2) and ...)                  ->
            (... and not (1 or 2) and ...)              -> (... and not 1 and not 2 and ...)
            (... and not (1 and 2) and ...)             ->
            not(... and (1 and 2) and ...)              -> not(... and 1 and 2 and ...)
            not(... and (1 or 2) and ...)               ->
            not(... and not (1 or 2) and ...)           -> not(... and not 1 and not 2 and ...)
            not(... and not (1 and 2) and ...)          ->
            (... or (1 or 2) or ...)                    -> (... or 1 or 2 or ...)
            (... or (1 and 2) or ...)                   ->
            (... or not (1 and 2) or ...)               -> (... or not 1 or not 2 or ...)
            (... or not (1 or 2) or ...)                ->
            not(... or (1 or 2) or ...)                 -> not(... or 1 or 2 or ...)
            not(... or (1 and 2) or ...)                ->
            not(... or not (1 and 2) or ...)            -> not(... or not 1 or not 2 or ...)
            not(... or not (1 or 2) or ...)             ->

            综上，如下两种情况下，需要做上移展开：
            - 子节点无 not，且与父节点 logic 相同
            - 子节点有 not，且于父节点 logic 相反
        3.使用德摩根定律，去掉所有节点的 not
            这一点是否进行，由入参 de_morgan 决定

        :param de_morgan: 是否使用 德摩根 定律，去掉所有节点的 not
        :return:
        """
        if not self.child_nodes:
            return self

        # list of (parent, to_process_index, new_child_nodes)
        node_stack: List[Tuple[LogicTree, int, list]] = [(self, 0, [])]
        visited = set()
        while node_stack:
            parent, index, new_child_nodes = node_stack[-1]
            if de_morgan and index == 0:
                """使用德摩根定律，去掉节点的 not
                not (A and B)   == not A or not B
                not (A or B)    == not A and not B

                :param recursive: 
                :return: 
                """
                parent.de_morgan()

            # 此处要求 parent.child_nodes[index] 必定存在
            ch: Union[LogicTree, str] = parent.child_nodes[index]
            # 标志是否移动到下一个节点
            to_next = True
            if not isinstance(ch, LogicTree) or self.is_leaf_node():
                # ch 是叶子节点 如 '1'
                new_child_nodes.append(ch)
            elif ch.child_nodes:
                # ch 不是空节点  ch: {'child_nodes': [...]}
                if id(ch) not in visited:
                    # 如果该子节点的子节点未被处理过，将其压入栈中，等处理完它后，再返回来处理 ch
                    # 注意，此时不移动到下一个节点
                    node_stack.append((ch, 0, []))
                    to_next = False
                else:
                    new_child_nodes.append(ch)
            if to_next:
                if index < len(parent.child_nodes) - 1:
                    # 如果后续还有子节点
                    node_stack[-1] = (parent, index + 1, new_child_nodes)
                else:
                    # 已经处理完 parent 的所有子节点
                    if len(new_child_nodes) == 1:
                        # parent 中经过化简后，只有一个子节点
                        # parent: {'child_nodes': [x], 'inverse': True/False}
                        # x 可能是如下几种情况：
                        # 1             -> 1 / not 1
                        # not 1         -> not 1 / 1
                        # 1 or 2        -> 1 or 2  /  not (1 or 2)
                        # not (1 or 2)  -> not (1 or 2)  /  1 or 2
                        unique_grandson = new_child_nodes[0]
                        if isinstance(unique_grandson, LogicTree):
                            new_child_nodes = unique_grandson.child_nodes
                            parent.inverse = parent.inverse ^ unique_grandson.inverse
                            if len(unique_grandson.child_nodes) > 1:
                                parent.logic = unique_grandson.logic
                        else:
                            # 1 -> 1 / not 1  是否有 not 由 parent.inverse 决定
                            new_child_nodes = [unique_grandson]
                    if len(new_child_nodes) > 1:
                        # 当 parent 化简后存在多个子节点时，判定各个子节点是否可以上提展开
                        # 此处 parent.inverse 保持不变
                        new_child_nodes2 = []
                        for ch in new_child_nodes:
                            # ch 可能是如下几种情况：
                            # 1             -> 1
                            # not 1         -> not 1
                            # 1 or 2        -> 1 or 2
                            # not (1 or 2)  -> not (1 or 2)  /  not 1 and not 2
                            if not isinstance(ch, LogicTree) or ch.is_leaf_node():
                                new_child_nodes2.append(ch)
                                continue
                            if not ch.inverse:
                                if ch.logic == parent.logic:
                                    # 上提展开 (... or (1 or 2) or ...)
                                    new_child_nodes2.extend(ch.child_nodes)
                                else:
                                    # (... and (1 or 2) and ...)
                                    new_child_nodes2.append(ch)
                            elif ch.logic != parent.logic:
                                # not (1 or 2) 且 logic 相反
                                # 如 (... and not (1 or 2) and ...) -> (... and not 1 and not 2 and ...)
                                for grandson in ch.child_nodes:
                                    if not isinstance(grandson, LogicTree):
                                        # 1 -> not 1
                                        grandson = LogicTree([grandson], None, True)
                                    elif len(grandson.child_nodes) == 1:
                                        # {'child_nodes': [1], 'inverse': True} -> 1
                                        grandson = grandson.child_nodes[0]
                                    else:
                                        grandson.inverse = not grandson.inverse
                                    new_child_nodes2.append(grandson)
                            else:
                                # (... or not (1 or 2) or ...)
                                new_child_nodes2.append(ch)
                        new_child_nodes = new_child_nodes2
                    parent.child_nodes = new_child_nodes
                    node_stack.pop(-1)
                    visited.add(id(parent))
        return self

    def merge_other(self, other: 'LogicTree',
                    /, *, logic: Literal['or', 'and'] = 'and', recursive: bool = False, ) -> 'LogicTree':
        """将另一个 逻辑树 合并进来

        :param other:
        :param logic:
        :param recursive: 缺省为 False 时，merge 后 self 和 other 可能会发生共享引用，为 True 时则 merge 后完全互相独立
        :return:
        """
        # 为降低复杂度，去掉 inverse=True
        self.de_morgan()
        other.de_morgan()
        if logic == 'and':
            if self.logic == 'and':
                if other.logic == 'and':
                    # 可合并  a and b and c and d
                    self.child_nodes.extend(other.child_nodes if not recursive
                                            else [ch.copy(recursive=True) for ch in other.child_nodes])
                else:
                    # 不可合并 a and b and (c or d)
                    self.child_nodes.append(other if not recursive else other.copy(recursive=True))
            else:
                copy_self = self.copy(recursive=False)
                self.logic = 'and'
                if other.logic == 'and':
                    # 不可合并 (a or b) and c and d
                    self.child_nodes = other.child_nodes.copy() if not recursive \
                        else [ch.copy(recursive=True) for ch in other.child_nodes]
                    self.child_nodes.append(copy_self)
                else:
                    # 不可合并 (a or b) and (c or d)
                    self.child_nodes = [copy_self, other if not recursive else other.copy(recursive=True)]
        else:
            # self or other
            if self.logic == 'and':
                copy_self = self.copy(recursive=False)
                self.logic = 'or'
                if other.logic == 'and':
                    # 可合并  a and b or c and d
                    self.child_nodes = [copy_self, other if not recursive else other.copy(recursive=True)]
                else:
                    # self 并入 other  a and b or c or d
                    self.child_nodes = [copy_self]
                    self.child_nodes.extend(other.child_nodes if not recursive
                                            else [ch.copy(recursive=True) for ch in other.child_nodes])
            else:
                if other.logic == 'and':
                    # other 并入 self  a or b or c and d
                    self.child_nodes = [*self.child_nodes, other if not recursive else other.copy(recursive=True)]
                else:
                    # 可合并 a or b or c or d
                    self.child_nodes.extend(other.child_nodes if not recursive
                                            else [ch.copy(recursive=True) for ch in other.child_nodes])
        return self

    def merge_leaf_values(self, *leaf_values: str,
                          inverse: bool = False,
                          logic: Literal['or', 'and'] = 'and',
                          insert_head: bool = False) -> 'LogicTree':
        """将一个叶子节点合并进来

        :param leaf_values:
        :param inverse:
        :param logic:
        :param insert_head: 是否插入到子节点列表的头部，默认是追加到尾部
        :return:
        """
        if not leaf_values:
            return self
        # self 是非叶子节点
        if logic == 'and':
            if self.logic in {'and', None}:
                self.logic = 'and'
                # self.a and self.b and new
                if self.inverse:
                    inverse = not inverse
                self._extend_leaf_values(*leaf_values, inverse=inverse, insert_head=insert_head)

                return self
            # (self.a or self.b) and new
            self.child_nodes = [self.copy(recursive=True)] if len(self.child_nodes) else []
            self.logic = 'and'
            self._extend_leaf_values(*leaf_values, inverse=inverse, insert_head=insert_head)
            self.inverse = False
            return self
        if self.logic == 'and':
            # self.a and self.b or new
            self.child_nodes = [self.copy(recursive=True)] if len(self.child_nodes) else []
            self.logic = 'or'
            self._extend_leaf_values(*leaf_values, inverse=inverse, insert_head=insert_head)
            self.inverse = False
            return self
        # self.a or self.b or cu
        self.logic = 'or'
        if self.inverse:
            inverse = not inverse
        self._extend_leaf_values(*leaf_values, inverse=inverse, insert_head=insert_head)
        return self

    def _extend_leaf_values(self, *leaf_values: str, inverse: bool, insert_head: bool = False):
        if inverse:
            leaf_values = [LogicTree([v], inverse=True) for v in leaf_values]
        if insert_head:
            self.child_nodes[:0] = leaf_values
        else:
            self.child_nodes.extend(leaf_values)

    def to_str(self, /, *, line_feed: bool = True, indent: int = 0) -> str:
        """转换为 string 形式

        :param line_feed: 是否换行
        :param indent: 换行时多层之间的的缩进量
        :return:
        """
        if line_feed:
            return self.to_str_as_multi_lines(indent=indent)
        return self.to_str_as_one_line()

    def to_str_as_one_line(self, /, ) -> str:
        """

        :return: '{1} and {2} and ({30} or {31} and {32} or (({41} or {42}) and {43} or {44})) and {50}'
        """
        if not self.child_nodes:
            return ''
        parts = []
        for ch in self.child_nodes:
            if not isinstance(ch, LogicTree):
                # 如果是个叶子值，注意，当 self 只有 1 个叶子节点时，目前处理流程下，not 只能作为整体的 not 而处理
                # 如 not 1, 只能在后续再加上前面的 not
                tmp = self._leaf_as_str(ch, False, )
            elif ch.is_leaf_node():
                # ch 是个1个叶子节点
                # 如 {'child_nodes': ['1'], 'inverse': True}
                tmp = self._leaf_as_str(ch.child_nodes[0], ch.inverse, )
            else:
                tmp = ch.to_str_as_one_line()
                if not ch.inverse and ch.logic == 'or':
                    tmp = '(' + tmp + ')'
            parts.append(tmp)
        res = (' ' + str(self.logic) + ' ').join(parts) if len(parts) > 1 else parts[0]
        if self.inverse:
            if self.is_leaf_node():
                # 当该节点是个叶子节点时
                res = "not " + res
            else:
                # not ({8} and {9})
                res = "not (%s)" % (res,)
        return res

    def to_str_as_multi_lines(self, /, *, indent: int = 0, ) -> str:
        """

        :param indent:
        :return:
            {1}
            and {2}
            and (
                {30}
                or
                    {31}
                    and {32}
                or (
                        (
                            {41}
                            or {42}
                        )
                        and {43}
                    or {44}
                )
            )
            and {50}
        """
        if not self.child_nodes:
            return ''
        holder = PlaceHolder(set(self.collect_leaf_values().keys()))
        result = '%(node_0)s'
        # list of (占位符，node，缩进)
        nodes: List[Tuple[str, LogicTree]] = [('node_0', self)]
        level = 0
        while nodes:
            nodes_next = []
            holder_node_strings = {}
            for node_holder, node in nodes:
                # 计算每个 node 的字符串
                node_string, sub_nodes = node._to_str_with_holder(holder, indent=indent + 4 * level)
                holder_node_strings[node_holder] = node_string
                nodes_next.extend(sub_nodes)
            result = result % holder_node_strings
            nodes = nodes_next
            level += 1
        return result

    def _to_str_with_holder(self, holder: PlaceHolder,
                            /, *, indent: int = 0) -> Tuple[str, List[Tuple[str, 'LogicTree']]]:
        sub_nodes_new = []
        mid_rows = []
        for ch in self.child_nodes:
            if not isinstance(ch, LogicTree):
                # 如果是个叶子值，注意，当 self 只有 1 个叶子节点时，目前处理流程下，not 只能作为整体的 not 而处理
                # 如 not 1, 只能在后续再加上前面的 not
                tmp = self._leaf_as_str(ch, False, )
                if not mid_rows:
                    tmp = ' ' * indent + tmp
            elif ch.is_leaf_node():
                # ch 是个叶子节点
                # 如 {'child_nodes': ['1'], 'inverse': True}
                tmp = self._leaf_as_str(ch.child_nodes[0], ch.inverse, )
                if not mid_rows:
                    tmp = ' ' * indent + tmp
            else:
                holder_new = holder.get_new_holder()
                tmp = '%({})s'.format(holder_new)
                new_line_canceled = False
                if not ch.inverse and ch.logic == 'or':
                    """ch 没有 not，且是 or 节点，需要此时加上括号                    
                    and 
                        (
                        {8}
                        or {9}
                        )
                    ch 有 not 时，在 ch.to_str_as_multi_lines() 中已经处理
                    """
                    if not mid_rows:
                        # 如果是第一个节点，加上前置缩进
                        tmp = "%s(\n%s\n%s)" % (' ' * indent, tmp, ' ' * indent)
                    else:
                        # 如果不是第一个节点，不用加缩进，因为会被格式化为 ... and/or (tmp
                        tmp = "(\n%s\n%s)" % (tmp, ' ' * indent)
                        # 且为了美观，此时在其前面不加换行
                        new_line_canceled = True
                if mid_rows and not new_line_canceled:
                    """对于复合节点，且 不是第一个子节点时，需要加换行，如
                    {1}
                    or 
                        {2}
                        and {3}
                    """
                    tmp = '\n' + tmp
                sub_nodes_new.append((holder_new, ch))
            mid_rows.append(tmp)
        if len(mid_rows) > 1:
            res = ('\n' + ' ' * indent + str(self.logic) + ' ').join(mid_rows)
        else:
            res = mid_rows[0]
        if self.inverse:
            # 该节点整体有 not
            if self.is_leaf_node():
                # 当该节点是一个叶子节点
                res = "%snot %s" % (' ' * indent, res)
            else:
                """
                not (
                    {8}
                    and {9}
                )
                """
                res = "%snot (\n%s\n%s)" % (' ' * indent, res, ' ' * indent)
        return res, sub_nodes_new

    @classmethod
    def _leaf_as_str(cls, leaf_value: str, inverse: bool, /, ) -> str:
        tmp = '{' + str(leaf_value) + '}'
        if inverse:
            tmp = 'not ' + tmp
        return tmp

    @classmethod
    def new_from_str(cls, logic_str: str, /) -> 'LogicTree':
        """Create a logic tree from a string.

        :param logic_str: like '{1} or {2}'
        :return:
        """
        if not logic_str:
            return cls()
        dic = parse_logic_str(logic_str)
        return cls.new_from_dict(dic)

    @classmethod
    def new_from_dict(cls, logic_dict: dict, data_name: str = 'givenLogicDict', /) -> 'LogicTree':
        """Create a logic tree from a dict.
        Note: Recursive Reference in logic dict will raise recursive cycle.

        :param logic_dict: like {'child_nodes': [1, 2], 'logic': 'or', 'inverse': False}
        :param data_name: help generate more accurate error messages when exceptions occur
        :return:
        """
        if not logic_dict or not logic_dict.get('child_nodes'):
            return cls()
        # list of (node_dic, node_name, to_process_child_index, final_child_nodes)
        node_stack: List[Tuple[dict, str, int, List[Union[str, LogicTree]]]] = [(logic_dict, data_name, 0, [])]
        # dict of id(node_dic): node
        visited: Dict[int, Union[LogicTree, None]] = {}
        while node_stack:
            node_dic, node_name, index, final_child_nodes = node_stack[-1]

            # 注意：此处要求 node_dic['child_nodes'][index]
            ch_value = node_dic['child_nodes'][index]
            ch_name = "%s['child_nodes'][%s]" % (data_name, index)
            # 标志是否移动到下一个节点
            to_next = True

            if isinstance(ch_value, dict):
                if ch_value and ch_value.get('child_nodes'):
                    # ch 不是空节点  ch: {'child_nodes': [...]}
                    if id(ch_value) not in visited:
                        # 如果该子节点的子节点未被处理过，将其压入栈中，等处理完它后，再返回来处理 ch
                        # 注意，此时不移动到下一个节点
                        node_stack.append((ch_value, ch_name, 0, []))
                        to_next = False
                    elif visited[id(ch_value)]:
                        # 不是空节点
                        final_child_nodes.append(visited[id(ch_value)])
            else:
                # ch 是叶子节点
                if ch_value == '':
                    raise ValueError("%s cannot be empty string." % (ch_name,))
                final_child_nodes.append(ch_value)
            if to_next:
                if index < len(node_dic['child_nodes']) - 1:
                    # 如果后续还有子节点
                    node_stack[-1] = (node_dic, node_name, index + 1, final_child_nodes)
                else:
                    new_inst = cls(final_child_nodes)
                    if final_child_nodes:
                        # 已经处理完 node_dic['child_nodes'] 中全部子节点
                        # 如果存在至少一个有效的子节点
                        if 'inverse' in node_dic:
                            if node_dic['inverse'] in {None, False, 'false', 'False', 'FALSE', 0, 'n', 'N', 'no', 'NO'}:
                                new_inst.inverse = False
                            elif node_dic['inverse'] in {True, 'true', 'True', 'TRUE', 1, 'y', 'Y', 'yes', 'YES'}:
                                new_inst.inverse = True
                            else:
                                raise ValueError("%s['inverse'] value error." % (node_name,))
                        if 'logic' in node_dic:
                            if node_dic['logic'] in {None, 'and', 'AND', False, 0}:
                                new_inst.logic = 'and'
                            elif node_dic['logic'] in {'or', 'OR', True, 1, }:
                                new_inst.logic = 'or'
                            else:
                                raise ValueError("%s['logic'] value error." % (node_name,))
                        visited[id(node_dic)] = new_inst
                    else:
                        visited[id(node_dic)] = None
                    if len(node_stack) == 1:
                        return new_inst
                    node_stack.pop(-1)
        return cls()

    def to_dict(self) -> dict:
        """Return dict copy of self.

        :return:
        """
        if not self.child_nodes:
            return {'child_nodes': []}
        # list of (node, to_process_child_index, final_child_nodes)
        node_stack: List[Tuple[LogicTree, int, List[Union[dict, str]]]] = [(self, 0, [])]
        # dict of id(node_dic): node:
        visited: Dict[int, Union[dict, None]] = {}
        while node_stack:
            node, index, final_child_nodes = node_stack[-1]

            # 注意：此处要求 node.child_nodes[index]
            ch_node = node.child_nodes[index]
            # 标志是否移动到下一个节点
            to_next = True

            if isinstance(ch_node, LogicTree):
                if ch_node.is_leaf_node():
                    # 如果是叶子节点
                    if ch_node.inverse:
                        final_child_nodes.append({'child_nodes': [ch_node.child_nodes[0]], 'inverse': True})
                    else:
                        final_child_nodes.append(ch_node.child_nodes[0])
                elif ch_node.child_nodes:
                    # ch 不是空节点  ch: {'child_nodes': [...]}
                    if id(ch_node) not in visited:
                        # 如果该子节点的子节点未被处理过，将其压入栈中，等处理完它后，再返回来处理 ch
                        # 注意，此时不移动到下一个节点
                        node_stack.append((ch_node, 0, []))
                        to_next = False
                    elif visited[id(ch_node)]:
                        # 不是空节点
                        final_child_nodes.append(visited[id(ch_node)])
            else:
                # ch 是叶子值
                final_child_nodes.append(ch_node)
            if to_next:
                if index < len(node.child_nodes) - 1:
                    # 如果后续还有子节点
                    node_stack[-1] = (node, index + 1, final_child_nodes)
                else:
                    node_dic = {'child_nodes': final_child_nodes, }
                    if final_child_nodes:
                        # 已经处理完 node_dic['child_nodes'] 中全部子节点
                        # 如果存在至少一个有效的子节点
                        if node.inverse:
                            node_dic['inverse'] = True
                        if len(final_child_nodes) > 1 or node.logic == 'or':
                            node_dic['logic'] = node.logic
                        visited[id(node)] = node_dic
                    else:
                        visited[id(node)] = None
                    if len(node_stack) == 1:
                        return node_dic
                    node_stack.pop(-1)
        return {'child_nodes': []}
