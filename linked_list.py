from typing import List, Optional, Union


class OutOfBoundsException(Exception):
    pass


class LinkedListNode(object):
    """
    Nó de uma lista ligada. Esta estrutura recebe um valor
    e o apontador para o próximo nó, que pode ser nulo
    """

    def __init__(self, value: Union[int, str, float], next: Optional['LinkedListNode'] = None):
        self._value = value
        self._next = next

    @property
    def value(self) -> Union[int, str, float]:
        """
        Retorna o valor do nó atual
        """
        return self._value

    @property
    def next(self) -> Optional['LinkedListNode']:
        """
        Retorna o apontador para o próximo nó
        """
        return self._next

    @next.setter
    def next(self, node: 'LinkedListNode'):
        """
        Define o apontador para o próximo nó
        """
        self._next = node

    def hasNext(self) -> bool:
        """
        Retorna True se existir um próximo nó, False caso contrário
        """
        return self._next is not None


class LinkedList(object):
    def __init__(self):
        """
        Construtor de lista ligada. A lista sempre começa vazia
        """
        self._head = None
        self._tail = None
        self._len = 0

    def __len__(self) -> int:
        return self._len

    @property
    def head(self) -> Optional[Union[int, str, float]]:
        """
        Esta propriedade deve retornar o valor do primeiro nó da lista ligada
        """
        if not self._head:
            return None
        return self._head.value

    @property
    def tail(self) -> Optional[Union[int, str, float]]:
        """
        Esta propriedade deve retornar o valor do último nó da lista ligada
        """
        if not self._tail:
            return None
        return self._tail.value

    def append(self, value: Union[int, str, float]):
        """
        Esta função deve inserir um novo nó no FINAL da lista ligada com valor value.
        Após a execução desta função a lista ligada deve ter um elemento a mais.
        """
        new_node = LinkedListNode(value)
        if not self._head:
            self._head = new_node
            self._tail = self._head
        else:
            self._tail.next = new_node
            self._tail = new_node
        self._len += 1

    def insert(self, value: Union[int, str, float]):
        """
        Esta função deve inserir um novo nó no INICIO da lista ligada com valor value.
        Após a execução desta função a lista ligada deve ter um elemento a mais.
        """
        new_node = LinkedListNode(value, self._head)
        if not self._tail:
            self._tail = new_node
        self._head = new_node
        self._len += 1

    def removeFirst(self) -> Optional[Union[int, str, float]]:
        """
        Esta função deve remover o primeiro elemento da lista e retornar o seu valor.
        Após a execução, a lista ligada deve ter um elemento a menos.
        """
        if not self._head:
            return None
        removed_value = self._head.value
        self._head = self._head.next
        if not self._head:
            self._tail = None
        self._len -= 1
        return removed_value

    def getValueAt(self, index: int) -> Union[int, str, float]:
        """
        Esta função deve retornar o valor de um nó na posição definida por INDEX.
        Se o index for maior do que o tamanho da lista, retornar OutOfBoundsException
        """
        if index >= self._len or index < 0:
            raise OutOfBoundsException("Index out of bounds")
        current = self._head
        for i in range(index):
            current = current.next
        return current.value

    def toList(self) -> List[Union[int, str, float]]:
        """
        Esta função retorna uma representação em forma de vetor ([1, 2, 3....])
        da lista ligada
        """
        result = []
        current = self._head
        while current:
            result.append(current.value)
            current = current.next
        return result


if __name__ == "__main__":
    """
    Gabarito de execução e testes. Se o seu código passar e chegar até o final,
    possivelmente você implementou tudo corretamente
    """
    ll = LinkedList()
    assert(ll.head is None)
    assert(ll.tail is None)
    assert(ll.toList() == [])
    ll.append(1)
    assert(ll.head == 1)
    assert(ll.tail == 1)
    assert(len(ll) == 1)
    assert(ll.toList() == [1])
    ll.append(2)
    assert(ll.head == 1)
    assert(ll.tail == 2)
    assert(len(ll) == 2)
    assert(ll.toList() == [1, 2])
    ll.append(3)
    assert(ll.head == 1)
    assert(ll.tail == 3)
    assert(len(ll) == 3)
    assert(ll.toList() == [1, 2, 3])
    ll.insert(0)
    assert(ll.head == 0)
    assert(ll.tail == 3)
    assert(len(ll) == 4)
    assert(ll.toList() == [0, 1, 2, 3])
    ll.insert(-1)
    assert(ll.toList() == [-1, 0, 1, 2, 3])
    v = ll.removeFirst()
    assert(v == -1)
    assert(ll.toList() == [0, 1, 2, 3])
    v = ll.removeFirst()
    assert(v == 0)
    assert(ll.toList() == [1, 2, 3])
    v = ll.removeFirst()
    assert(v == 1)
    assert(ll.toList() == [2, 3])
    v = ll.removeFirst()
    assert(v == 2)
    assert(ll.toList() == [3])
    v = ll.removeFirst()
    assert(v == 3)
    assert(ll.toList() == [])
    assert(len(ll) == 0)
    print("100%")
