# Mulltiprocessing --- 프로세스 기반 병렬 처리

소스 코드: Lib/multiprocessing/
<https://docs.python.org/ko/3/library/multiprocessing.html>
<https://docs.python.org/ko/3/library/index.html>

## 소개

- multiprocessing 은 threading 모듈과 유사한 API를 사용하여 프로세스 스포닝(spawning)을 지원하는 패키지입니다.
- multiprocessing 패키지는 지역과 원격 동시성을 모두 제공하며 스레드 대신 서브 프로세스를 사용하여 전역 인터프리터 록 을 효과적으로 피합니다. 이것 때문에, multiprocessing 모듈은 프로그래머가 주어진 기계에서 다중 프로세서를 최대한 활용할 수 있게 합니다.
- 유닉스와 윈도우에서 모두 실행됩니다.

- multiprocessing 모듈은 threading 모듈에 대응 물이 없는 API도 제공합니다.
- 이것의 대표적인 예가 Pool 객체입니다. 이 객체는 여러 입력 값에 걸쳐 함수의 실행을 병렬 처리하고 입력 데이터를 프로세스에 분산시키는 편리한 방법을 제공합니다(데이터 병렬 처리).
- 다음 예제는 자식 프로세스가 해당 모듈을 성공적으로 임포트 할 수 있도록, 모듈에서 이러한 함수를 정의하는 일반적인 방법을 보여줍니다.
  
다음은 Pool 를 사용하는 데이터 병렬 처리의 기본 예제입니다:

```python
from multiprocessing import Pool

def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(5) as p:
        print(p.map(f, [1, 2, 3]))

# 실행
[1, 4, 9]
```

### Process 클래스

- multiprocessing에서, 프로세스는 Process 객체를 생성한 후 start() 메서드를 호출해서 스폰합니다.
- Process 는 threading.Thread 의 API를 따릅니다.
- 다중 프로세스 프로그램의 간단한 예는 다음과 같습니다

```python
from multiprocessing import Process

def f(name):
    print('hello', name)

if __name__ == '__main__':
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
```

이 과정에 참여하는 개별 프로세스의 ID를 보기 위해, 이렇게 예제를 확장합니다:

```process
from multiprocessing import Process
import os

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    info('function f')
    print('hello', name)

if __name__ == '__main__':
    info('main line')
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
```

`if __name__ == '__main__'` 부분이 필요한 이유에 대한 설명은 프로그래밍 지침을 보십시오.

### 컨텍스트 및 시작 방법

플랫폼에 따라, multiprocessing은 프로세스를 시작하는 세 가지 방법을 지원합니다. 이러한 시작 방법 은

- spawn
  - 부모 프로세스는 깨끗한 새 파이썬 인터프리터 프로세스를 시작합니다.
  - 자식 프로세스는 프로세스 객체의 run() 메서드를 실행하는데 필요한 자원만 상속받습니다.
  - 특히, 부모 프로세스의 불필요한 파일 기술자와 핸들은 상속되지 않습니다. 이 방법을 사용하여 프로세스를 시작하는 것은 fork나 forkserver 를 사용하는 것에 비해 다소 느립니다.
  - 유닉스 및 윈도우에서 사용 가능합니다. 윈도우의 기본값.

- fork
  - 부모 프로세스는 os.fork() 를 사용하여 파이썬 인터프리터를 포크 합니다.
  - 자식 프로세스는, 시작될 때, 부모 프로세스와 실질적으로 같습니다.
  - 부모의 모든 자원이 자식 프로세스에 의해 상속됩니다.
  - 다중 스레드 프로세스를 안전하게 포크 하기 어렵다는 점에 주의하십시오.
  - 유닉스에서만 사용 가능합니다. 유닉스의 기본값.

- forkserver
  - 프로그램이 시작되고 forkserver 시작 방법을 선택하면, 서버 프로세스가 시작됩니다. 그 이후부터, 새로운 프로세스가 필요할 때마다, 부모 프로세스는 서버에 연결하여 새로운 프로세스를 포크 하도록 요청합니다.
  - 포크 서버 프로세스는 단일 스레드이므로 os.fork() 를 사용하는 것이 안전합니다.
  - 불필요한 자원은 상속되지 않습니다.
  - 유닉스 파이프를 통해 파일 기술자를 전달할 수 있는 유닉스 플랫폼에서 사용할 수 있습니다.

버전 3.4에서 변경: 모든 유닉스 플랫폼에 spawn 이 추가되었고, 일부 유닉스 플랫폼에는 forkserver 가 추가되었습니다. 윈도우에서 자식 프로세스는 상속 가능한 모든 부모 핸들을 더는 상속하지 않습니다.

유닉스에서 spawn 또는 forkserver 시작 방법을 사용하면 세마포어 추적기 프로세스 역시 시작되는데, 프로그램의 프로세스들이 만든 삭제되지 않은 이름있는 세마포어를 추적합니다. 모든 프로세스가 종료된 후 세마포어 추적기는 남아있는 세마포어를 제거합니다. 일반적으로 아무것도 남아 있지 않아야 하지만, 프로세스가 시그널에 의해 죽으면 "누수된" 세마포어가 있을 수 있습니다. (이름있는 세마포어의 제거는 심각한 문제인데, 시스템이 제한된 수만 허용하고 다음 재부팅 때까지 자동으로 제거되지 않기 때문입니다.)

시작 방법을 선택하려면 메인 모듈의 `if __name__ == '__main__'` 절에서 set_start_method()를 사용하십시오. 예를 들면:

```python
import multiprocessing as mp

def foo(q):
    q.put('hello')

if __name__ == '__main__':
    mp.set_start_method('spawn')
    q = mp.Queue()
    p = mp.Process(target=foo, args=(q,))
    p.start()
    print(q.get())
    p.join()
```

set_start_method() 는 프로그램에서 한 번만 사용되어야 합니다.

또는, get_context()를 사용하여 컨텍스트 객체를 얻을 수 있습니다. 컨텍스트 객체는 multiprocessing 모듈과 같은 API를 제공하므로 한 프로그램에서 여러 시작 방법을 사용할 수 있습니다.

```python
import multiprocessing as mp

def foo(q):
    q.put('hello')

if __name__ == '__main__':
    ctx = mp.get_context('spawn')
    q = ctx.Queue()
    p = ctx.Process(target=foo, args=(q,))
    p.start()
    print(q.get())
    p.join()
```

한 컨텍스트와 관련된 객체는 다른 컨텍스트의 프로세스와 호환되지 않을 수 있음에 주의하십시오. 특히 fork 컨텍스트를 사용하여 생성된 록은 spawn 또는 forkserver 시작 방법을 사용하여 시작된 프로세스로 전달될 수 없습니다.

특정 시작 방법을 사용하고자 하는 라이브러리는 아마도 get_context()를 사용하여 라이브러리 사용자의 선택을 방해하지 않아야 합니다.

>> 경고 'spawn' 과 'forkserver' 시작 방법은 현재 유닉스에서 "고정된(frozen)" 실행 파일(즉, PyInstaller와 cx_Freeze와 같은 패키지로 만든 바이너리)과 함께 사용할 수 없습니다. 'fork' 시작 방법은 작동합니다.

### 프로세스 간 객체 교환

multiprocessing 은 두 가지 유형의 프로세스 간 통신 채널을 지원합니다:

#### 큐

Queue 클래스는 queue.Queue 의 클론에 가깝습니다. 예를 들면:

```python
from multiprocessing import Process, Queue

def f(q):
    q.put([42, None, 'hello'])

if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    print(q.get())    # prints "[42, None, 'hello']"
    p.join()
```

큐는 스레드와 프로세스에 안전합니다.

#### 파이프

Pipe() 함수는 파이프로 연결된 한 쌍의 연결 객체를 돌려주는데 기본적으로 양방향(duplex)입니다. 예를 들면:

```python
from multiprocessing import Process, Pipe

def f(conn):
    conn.send([42, None, 'hello'])
    conn.close()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    print(parent_conn.recv())   # prints "[42, None, 'hello']"
    p.join()
```

Pipe() 가 반환하는 두 개의 연결 객체는 파이프의 두 끝을 나타냅니다. 각 연결 객체에는 (다른 것도 있지만) send() 및 recv() 메서드가 있습니다. 두 프로세스 (또는 스레드)가 파이프의 같은 끝에서 동시에 읽거나 쓰려고 하면 파이프의 데이터가 손상될 수 있습니다. 물론 파이프의 다른 끝을 동시에 사용하는 프로세스로 인해 손상될 위험은 없습니다.

### 프로세스 간 동기화

multiprocessing 은 threading 에 있는 모든 동기화 프리미티브의 등가물을 포함합니다. 예를 들어 한 번에 하나의 프로세스만 표준 출력으로 인쇄하도록 록을 사용할 수 있습니다:

```python
from multiprocessing import Process, Lock

def f(l, i):
    l.acquire()
    try:
        print('hello world', i)
    finally:
        l.release()

if __name__ == '__main__':
    lock = Lock()

    for num in range(10):
        Process(target=f, args=(lock, num)).start()
```

록을 사용하지 않으면 다른 프로세스의 출력들이 모두 섞일 수 있습니다.

### 프로세스 간 상태 공유

위에서 언급했듯이, 동시성 프로그래밍을 할 때 보통 가능한 한 공유된 상태를 사용하지 않는 것이 최선입니다. 여러 프로세스를 사용할 때 특히 그렇습니다.

그러나, 정말로 공유 데이터를 사용해야 한다면 multiprocessing 이 몇 가지 방법을 제공합니다.

#### 공유 메모리

데이터는 Value 또는 Array를 사용하여 공유 메모리 맵에 저장 될 수 있습니다. 예를 들어, 다음 코드는

```python
from multiprocessing import Process, Value, Array

def f(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]

if __name__ == '__main__':
    num = Value('d', 0.0)
    arr = Array('i', range(10))

    p = Process(target=f, args=(num, arr))
    p.start()
    p.join()

    print(num.value)
    print(arr[:])

# 결과
3.1415927
[0, -1, -2, -3, -4, -5, -6, -7, -8, -9]
```

num 과 arr 을 만들 때 사용되는 'd' 와 'i' 인자는 array 모듈에서 사용되는 종류의 타입 코드입니다: 'd' 는 배정밀도 부동 소수점을 나타내고, 'i' 는 부호 있는 정수를 나타냅니다. 이러한 공유 객체는 프로세스 및 스레드에 안전합니다.

공유 메모리를 더 유연하게 사용하려면, 공유 메모리에 할당된 임의의 ctypes 객체 생성을 지원하는 multiprocessing.sharedctypes 모듈을 사용할 수 있습니다.

#### 서버 프로세스

Manager() 가 반환한 관리자 객체는 파이썬 객체를 유지하고 다른 프로세스가 프락시를 사용하여 이 객체를 조작할 수 있게 하는 서버 프로세스를 제어합니다.

Manager() 가 반환한 관리자는 list, dict, Namespace, Lock, RLock, Semaphore, BoundedSemaphore, Condition, Event, Barrier, Queue, Value 그리고 Array 형을 지원합니다. 예를 들어, 다음 코드는

```python
from multiprocessing import Process, Manager

def f(d, l):
    d[1] = '1'
    d['2'] = 2
    d[0.25] = None
    l.reverse()

if __name__ == '__main__':
    with Manager() as manager:
        d = manager.dict()
        l = manager.list(range(10))

        p = Process(target=f, args=(d, l))
        p.start()
        p.join()

        print(d)
        print(l)
# 결과
{0.25: None, 1: '1', '2': 2}
[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
```

서버 프로세스 관리자는 임의의 객체 형을 지원하도록 만들 수 있으므로 공유 메모리 객체를 사용하는 것보다 융통성이 있습니다. 또한, 단일 관리자를 네트워크를 통해 서로 다른 컴퓨터의 프로세스에서 공유 할 수 있습니다. 그러나 공유 메모리를 사용할 때보다 느립니다.

### 작업자 풀 사용

Pool 클래스는 작업자 프로세스 풀을 나타냅니다. 여기에는 몇 가지 다른 방법으로 작업을 작업자 프로세스로 넘길 수 있는 메서드가 있습니다.

예를 들면:

```python
from multiprocessing import Pool, TimeoutError
import time
import os

def f(x):
    return x*x

if __name__ == '__main__':
    # start 4 worker processes
    with Pool(processes=4) as pool:

        # print "[0, 1, 4,..., 81]"
        print(pool.map(f, range(10)))

        # print same numbers in arbitrary order
        for i in pool.imap_unordered(f, range(10)):
            print(i)

        # evaluate "f(20)" asynchronously
        res = pool.apply_async(f, (20,))      # runs in *only* one process
        print(res.get(timeout=1))             # prints "400"

        # evaluate "os.getpid()" asynchronously
        res = pool.apply_async(os.getpid, ()) # runs in *only* one process
        print(res.get(timeout=1))             # prints the PID of that process

        # launching multiple evaluations asynchronously *may* use more processes
        multiple_results = [pool.apply_async(os.getpid, ()) for i in range(4)]
        print([res.get(timeout=1) for res in multiple_results])

        # make a single worker sleep for 10 secs
        res = pool.apply_async(time.sleep, (10,))
        try:
            print(res.get(timeout=1))
        except TimeoutError:
            print("We lacked patience and got a multiprocessing.TimeoutError")

        print("For the moment, the pool remains available for more work")

    # exiting the 'with'-block has stopped the pool
    print("Now the pool is closed and no longer available")
```

풀의 메서드는 풀을 만든 프로세스에서만 사용되어야 함에 유의하세요.

>> 참고 : 이 패키지 내의 기능을 사용하려면 __main__ 모듈을 자식이 임포트 할 수 있어야 합니다. 이것은 프로그래밍 지침에서 다루지만, 여기에서 지적할 가치가 있습니다. 이것은 몇몇 예제, 가령 multiprocessing.pool.Pool 예제가 대화형 인터프리터에서 동작하지 않음을 의미합니다. 예를 들면:

```python
from multiprocessing import Pool
p = Pool(5)

def f(x):
    return x*x

p.map(f, [1,2,3])

# 결과
Process PoolWorker-1:
Process PoolWorker-2:
Process PoolWorker-3:
Traceback (most recent call last):
AttributeError: 'module' object has no attribute 'f'
AttributeError: 'module' object has no attribute 'f'
AttributeError: 'module' object has no attribute 'f'
```

(이것을 시도해 보면 실제로 세 개의 전체 트레이스백이 어느 정도 임의로 번갈아 출력됩니다. 그런 다음 마스터 프로세스를 중지시켜야 할 수도 있습니다.)

## 레퍼런스

multiprocessing 패키지는 대부분 threading 모듈의 API를 복제합니다.

### Process와 예외

```python
class multiprocessing.Process(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None)
```

>> 프로세스 객체는 별도의 프로세스에서 실행되는 작업을 나타냅니다. Process 클래스는 threading.Thread 의 모든 메서드와 같은 메서드를 갖습니다.
>> 생성자는 항상 키워드 인자로 호출해야 합니다. group 은 항상 None 이어야 합니다; 이것은 threading.Thread 와의 호환성을 위해서만 존재합니다. target 은 run() 메서드에 의해 호출될 콜러블 객체입니다. 기본값은 None 인데, 아무것도 호출되지 않음을 의미합니다. name 은 프로세스 이름입니다 (자세한 내용은 name 참조). args 는 target 호출을 위한 인자 튜플입니다. kwargs 는 target 호출을 위한 키워드 인자 딕셔너리입니다. 제공되는 경우, 키워드 전용 daemon 인자는 프로세스 daemon 플래그를 True 또는 False 로 설정합니다. None (기본값) 이면, 이 플래그는 만드는 프로세스로부터 상속됩니다.
>> 기본적으로, 아무 인자도 target 에 전달되지 않습니다.
>> 서브 클래스가 생성자를 재정의하면, 프로세스에 다른 작업을 하기 전에 베이스 클래스 생성자(Process.__init__())를 호출해야 합니다.

버전 3.3에서 변경: daemon 인자가 추가되었습니다.

#### run()

프로세스의 활동을 나타내는 메서드.

서브 클래스에서 이 메서드를 재정의할 수 있습니다. 표준 run() 메서드는 객체의 생성자에 target 인자로 전달된 콜러블 객체를 호출하는데 (있다면) args 와 kwargs 인자를 각각 위치 인자와 키워드 인자로 사용합니다.

#### start()

프로세스의 활동을 시작합니다.

이것은 프로세스 객체 당 최대 한 번 호출되어야 합니다. 객체의 run() 메서드가 별도의 프로세스에서 호출되도록 합니다.

#### join([timeout])

선택적 인자 timeout 이 None (기본값) 인 경우, 메서드는 join() 메서드가 호출된 프로세스가 종료될 때까지 블록 됩니다. timeout 이 양수면 최대 timeout 초 동안 블록 됩니다. 이 메서드는 프로세스가 종료되거나 메서드가 시간 초과 되면 None 을 돌려줌에 주의해야 합니다. 프로세스의 exitcode 를 검사하여 종료되었는지 확인하십시오.

프로세스는 여러 번 조인할 수 있습니다.

교착 상태를 유발할 수 있으므로 프로세스는 자신을 조인할 수 없습니다. 프로세스가 시작되기 전에 프로세스에 조인하려고 하면 에러가 발생합니다.

#### name

프로세스의 이름. 이름은 식별 목적으로만 사용되는 문자열입니다. 다른 의미는 없습니다. 여러 프로세스에 같은 이름이 주어질 수 있습니다.

초기 이름은 생성자에 의해 설정됩니다. 명시적 이름이 생성자에 제공되지 않으면, 'Process-N1:N2:...:Nk' 형식의 이름이 만들어지는데, 각각의 Nk 는 부모의 N 번째 자식입니다.

#### is_alive()

프로세스가 살아있는지 아닌지를 반환합니다.

대략, 프로세스 객체는 start() 메서드가 반환하는 순간부터 자식 프로세스가 종료될 때까지 살아있습니다.

#### daemon

프로세스의 데몬 플래그, 논리값. start() 가 호출되기 전에 설정되어야 합니다.

초깃값은 생성 프로세스에서 상속됩니다.

프로세스가 종료할 때, 모든 데몬 자식 프로세스를 강제 종료시키려고(terminate) 시도합니다.

데몬 프로세스는 하위 프로세스를 만들 수 없음에 유의하십시오. 그렇지 않으면 부모 프로세스가 종료될 때 데몬 프로세스가 강제 종료되어, 데몬 프로세스가 자식 프로세스를 고아로 남기게 됩니다. 또한, 이들은 유닉스 데몬이나 서비스가 아닙니다, 데몬이 아닌 프로세스들이 종료되면 강제 종료되는 (그리고 조인되지 않는) 일반 프로세스입니다.

threading.Thread API 외에도 Process 객체는 다음 어트리뷰트와 메서드도 지원합니다 :

#### pid

프로세스 ID를 돌려줍니다. 프로세스가 스폰 되기 전에는 None 입니다.

#### exitcode

자식의 종료 코드. 프로세스가 아직 종료되지 않았으면 None 이 됩니다. 음수 값 -N 은 자식이 시그널 N 에 의해 강제 종료되었음을 나타냅니다.

#### authkey

프로세스의 인증 키 (바이트열) 입니다.

multiprocessing 이 초기화될 때, 메인 프로세스는 os.urandom() 을 사용하여 임의의 문자열을 할당받습니다.

Process 객체가 생성될 때, 부모 프로세스의 인증 키를 상속받습니다. authkey 를 다른 바이트열로 설정하여 변경할 수 있습니다.

인증 키를 참조하세요.

#### sentinel

프로세스가 끝나면 "준비(ready)" 될 시스템 객체의 숫자 핸들.

multiprocessing.connection.wait() 를 사용해서 한 번에 여러 이벤트를 기다리고 싶다면, 이 값을 사용할 수 있습니다. 그렇지 않으면 join()을 호출하는 것이 더 간단합니다.

윈도우에서, 이것은 WaitForSingleObject 및 WaitForMultipleObjects 계열의 API 호출에서 사용할 수 있는 OS 핸들입니다. 유닉스에서, 이것은 select 모듈의 프리미티브들에서 사용할 수 있는 파일 기술자입니다.

버전 3.3에 추가.

#### terminate()

프로세스를 강제 종료합니다. 유닉스에서는 SIGTERM 시그널을 사용합니다; 윈도우에서는 TerminateProcess() 가 사용됩니다. 종료 처리기(exit handler)와 finally 절 등이 실행되지 않음에 주의하십시오.

프로세스의 자손 프로세스들은 강제 종료되지 않을 것입니다 -- 단순히 고아가 될 것입니다.

경고 연결된 프로세스가 파이프 또는 큐를 사용할 때 이 메서드를 사용하면, 파이프 또는 큐가 손상되어 다른 프로세스에서 사용할 수 없게 될 수 있습니다. 마찬가지로, 프로세스가 록이나 세마포어 등을 획득한 경우 강제 종료하면 다른 프로세스가 교착 상태가 될 수 있습니다.

#### kill()

terminate()와 같지만, 유닉스에서 SIGKILL 시그널을 사용합니다.

버전 3.7에 추가.

#### close()

Process 객체를 닫아, 그것과 관련된 모든 자원을 해제합니다. 하부 프로세스가 여전히 실행 중이면 ValueError 가 발생합니다. 일단 close() 가 성공적으로 반환되면, Process 객체의 다른 대부분의 메서드와 어트리뷰트는 ValueError 를 발생시킵니다.

버전 3.7에 추가.

start(), join(), is_alive(), terminate() 및 exitcode 메서드는 프로세스 객체를 생성한 프로세스에 의해서만 호출되어야 합니다.

Process 의 몇몇 메서드를 사용하는 예제:

```python
import multiprocessing, time, signal
p = multiprocessing.Process(target=time.sleep, args=(1000,))
print(p, p.is_alive())
<Process(Process-1, initial)> False
p.start()
print(p, p.is_alive())
<Process(Process-1, started)> True
p.terminate()
time.sleep(0.1)
print(p, p.is_alive())
<Process(Process-1, stopped[SIGTERM])> False
p.exitcode == -signal.SIGTERM
True
```

`exception multiprocessing.ProcessError`
모든 multiprocessing 예외의 베이스 클래스입니다.

`exception multiprocessing.BufferTooShort`
Connection.recv_bytes_into() 가, 제공된 버퍼 객체가 읽은 메시지에 비해 너무 작을 때 일으키는 예외.

e 가 BufferTooShort 의 인스턴스라면, e.args[0] 는 메시지를 바이트열로 줍니다.

`exception multiprocessing.AuthenticationError`
인증 에러가 일어날 때 발생합니다.

`exception multiprocessing.TimeoutError`
시간제한이 초과하였을 때 시간제한을 건 메서드에 의해 발생합니다.

### 파이프와 큐

여러 프로세스를 사용할 때, 일반적으로 프로세스 간 통신을 위해 메시지 전달을 사용하고 록과 같은 동기화 프리미티브 사용을 피합니다.

메시지를 전달하기 위해 Pipe() (두 프로세스 간의 연결) 또는 큐(여러 생산자와 소비자를 허용합니다)를 사용할 수 있습니다.

`Queue`, `SimpleQueue` 그리고 `JoinableQueue` 형은, 표준 라이브러리의 queue.Queue 클래스에 따라 모델링 된, 다중 생산자, 다중 소비자 FIFO 큐입니다. 이것들은 파이썬 2.5의 queue.Queue 클래스에서 도입된 task_done()과 join() 메서드가 Queue 에 없다는 점에서 다릅니다.

`JoinableQueue`를 사용하면, 큐에서 제거된 작업마다 JoinableQueue.task_done()을 호출해야 합니다. 그렇지 않으면 완료되지 않은 작업의 수를 세는 데 사용되는 세마포어가 결국 오버플로 되어 예외를 일으킵니다.

관리자 객체를 사용하여 공유 큐를 생성할 수도 있습니다 -- 관리자를 보세요.

- 참고 multiprocessing 은 제한 시간 초과 신호를 보내기 위해 보통 queue.Empty 와 queue.Full 예외를 사용합니다. multiprocessing 이름 공간에는 없으므로 queue에서 임포트 해야 합니다.

- 참고 객체를 큐에 넣으면, 객체는 피클 되고 배경 스레드가 나중에 피클 된 데이터를 하부 파이프로 플러시 합니다. 이것은 다소 의외의 결과로 이어지지만, 실제적인 어려움을 일으키지는 않아야 합니다 -- 이것이 여러분을 정말로 신경 쓰이게 한다면, 대신 관리자 로 만든 큐를 사용할 수 있습니다.
    1. 빈 큐에 객체를 넣은 후에, empty() 메서드가 False를 반환하고 get_nowait()가 queue.Empty 를 일으키지 않고 반환할 수 있기 전까지 극히 작은 지연이 있을 수 있습니다.
    2. 여러 프로세스가 객체를 큐에 넣는 경우, 반대편에서 객체가 다른 순서로 수신될 수 있습니다. 그러나, 같은 프로세스에 의해 큐에 들어간 객체들은 항상 상대적인 순서가 유지됩니다.

>> 경고 Queue를 사용하려고 하는 동안 Process.terminate() 또는 os.kill() 을 사용하여 프로세스를 죽이면, 큐의 데이터가 손상될 수 있습니다. 이로 인해 나중에 다른 프로세스가 큐를 사용하려고 할 때 예외가 발생할 수 있습니다.

>> 경고 위에서 언급했듯이, 자식 프로세스가 항목을 큐에 넣었을 때 (그리고 JoinableQueue.cancel_join_thread 를 사용하지 않았다면), 버퍼링 된 모든 항목이 파이프로 플러시 될 때까지 해당 프로세스가 종료되지 않습니다.
이것은, 여러분이 그 자식 프로세스를 조인하려고 하면, 큐에 넣은 모든 항목을 소진하지 않는 한 교착 상태가 발생할 수 있다는 뜻입니다. 마찬가지로, 그 자식 프로세스가 데몬이 아니면 부모 프로세스가 종료 시점에 데몬이 아닌 모든 자식을 조인하려고 할 때 정지될 수 있습니다.
관리자를 사용하여 생성된 큐에는 이 문제가 없습니다. 프로그래밍 지침을 참조하세요.

프로세스 간 통신을 위해 큐를 사용하는 예는 예제을 참조하십시오.

`multiprocessing.Pipe([duplex])`
파이프의 끝을 나타내는 Connection 객체 쌍 (conn1, conn2) 를 반환합니다.

duplex 가 True (기본값) 면 파이프는 양방향입니다. duplex 가 False 인 경우 파이프는 단방향입니다: conn1 은 메시지를 받는 데에만 사용할 수 있고, conn2 는 메시지를 보낼 때만 사용할 수 있습니다.

`class multiprocessing.Queue([maxsize])`
파이프와 몇 개의 록/세마포어를 사용하여 구현된 프로세스 공유 큐를 반환합니다. 프로세스가 처음으로 항목을 큐에 넣으면 버퍼에서 파이프로 객체를 전송하는 피더 스레드가 시작됩니다.

제한 시간 초과를 알리기 위해 표준 라이브러리의 queue 모듈에서 정의되는 queue.Empty 와 queue.Full 예외를 일으킵니다.

Queue 는 task_done()과 join() 을 제외한 queue.Queue 의 모든 메서드를 구현합니다.

qsize()
큐의 대략의 크기를 돌려줍니다. 다중 스레딩/다중 프로세싱 특성을 타기 때문에 이 숫자는 신뢰할 수 없습니다.

이것은 sem_getvalue() 가 구현되지 않은 Mac OS X와 같은 유닉스 플랫폼에서 NotImplementedError를 발생시킬 수 있습니다.

empty()
큐가 비어 있다면 True 를, 그렇지 않으면 False 를 반환합니다. 다중 스레딩/다중 프로세싱 특성을 타기 때문에 신뢰할 수 없습니다.

full()
큐가 가득 차면 True 를, 그렇지 않으면 False 를 반환합니다. 다중 스레딩/다중 프로세싱 특성을 타기 때문에 신뢰할 수 없습니다.

put(obj[, block[, timeout]])
obj를 큐에 넣습니다. 선택적 인자 block 이 True (기본값)이고 timeout 이 None (기본값) 이면, 빈 슬롯이 생길 때까지 필요한 경우 블록합니다. timeout 이 양수인 경우, 최대 timeout 초만큼 블록하고 그 시간 내에 사용 가능 슬롯이 생기지 않으면 queue.Full 예외를 발생시킵니다. 그렇지 않으면 (block 이 False) 빈 슬롯을 즉시 사용할 수 있으면 큐에 항목을 넣고, 그렇지 않으면 queue.Full 예외를 발생시킵니다 (이 경우 timeout 은 무시됩니다).

put_nowait(obj)
put(obj, False) 와 같습니다.

get([block[, timeout]])
큐에서 항목을 제거하고 반환합니다. 선택적 인자 block 이 True (기본값)이고 timeout 이 None (기본값) 이면, 항목이 들어올 때까지 필요한 경우 블록합니다. timeout 이 양수인 경우, 최대 timeout 초만큼 블록하고 그 시간 내에 항목이 들어오지 않으면 queue.Empty 예외를 발생시킵니다. 그렇지 않으면 (block이 False) 즉시 사용할 수 있는 항목이 있으면 반환하고, 그렇지 않으면 queue.Empty 예외를 발생시킵니다 (이 경우 timeout 은 무시됩니다).

get_nowait()
get(False) 와 같습니다.

multiprocessing.Queue 에는 queue.Queue 에서 찾을 수 없는 몇 가지 추가 메서드가 있습니다. 일반적으로 이러한 메서드는 대부분 코드에서 필요하지 않습니다:

close()
현재 프로세스가 이 큐에 더는 데이터를 넣지 않을 것을 나타냅니다. 버퍼에 저장된 모든 데이터를 파이프로 플러시 하면 배경 스레드가 종료됩니다. 큐가 가비지 수집될 때 자동으로 호출됩니다.

join_thread()
배경 스레드에 조인합니다. close() 가 호출된 후에만 사용할 수 있습니다. 배경 스레드가 종료될 때까지 블록해서 버퍼의 모든 데이터가 파이프로 플러시 되었음을 보증합니다.

기본적으로 프로세스가 큐를 만든 주체가 아니면 종료할 때 큐의 배경 스레드를 조인하려고 합니다. 프로세스는 cancel_join_thread()를 호출하여 join_thread() 가 아무것도 하지 않게 할 수 있습니다.

cancel_join_thread()
join_thread() 의 블록을 방지합니다. 특히, 프로세스가 종료할 때 배경 스레드를 자동으로 조인하는 것을 막습니다 -- join_thread()를 보십시오.

이 메서드의 더 좋은 이름은 allow_exit_without_flush() 일 것입니다. 큐에 포함된 데이터가 유실될 가능성이 크며, 거의 확실히 사용할 필요가 없을 겁니다. 현재 프로세스가 하부 파이프로 대기 중인 데이터를 플러시 할 때까지 기다리지 않고 즉시 종료해야 하고 데이터 손실에 대해서는 신경 쓰지 않을 때만을 위한 것입니다.

참고 이 클래스의 기능은 호스트 운영 체제의 작동하는 공유 세마포어 구현을 요구합니다. 그런 것이 없으면, 클래스의 기능이 비활성화되고, Queue 의 인스턴스를 만들려고 하면 ImportError 를 일으킵니다. 자세한 내용은 bpo-3770을 참조하십시오. 아래에 나열된 특수 큐 형들도 마찬가지입니다.
class multiprocessing.SimpleQueue
이것은 단순화된 Queue 형으로, 록이 걸린 Pipe 에 매우 가깝습니다.

empty()
큐가 비어 있다면 True 를, 그렇지 않으면 False 를 반환합니다.

get()
큐에서 항목을 제거하고 반환합니다.

put(item)
item 을 큐에 넣습니다.

class multiprocessing.JoinableQueue([maxsize])
Queue 서브 클래스 JoinableQueue 는 추가로 task_done()과 join() 메서드를 가진 큐입니다.

task_done()
앞서 큐에 넣은 작업이 완료되었음을 나타냅니다. 큐 소비자가 사용합니다. 작업을 가져오는데 사용된 각 get() 마다, 뒤따르는 task_done() 호출은 작업에 대한 처리가 완료되었음을 큐에 알립니다.

만약 join() 이 현재 블록하고 있다면, 모든 항목이 처리될 때 재개될 것입니다 (put() 으로 큐에 넣은 모든 항목에 대해 task_done() 호출을 수신했다는 뜻입니다).

큐에 있는 항목보다 많이 호출되면 ValueError 를 발생시킵니다.

join()
큐의 모든 항목을 가져가서 처리할 때까지 블록합니다.

항목이 큐에 추가될 때마다 완료되지 않은 작업의 수는 올라갑니다. 소비자가 그 항목을 꺼냈고 그에 대한 모든 작업을 완료했음을 알리기 위해 task_done()을 호출할 때마다 숫자는 줄어듭니다. 완료되지 않은 작업의 수가 0으로 떨어지면 join() 이 블록으로부터 풀려납니다.

### 잡동사니

multiprocessing.active_children()
현재 프로세스의 모든 살아있는 자식 리스트를 반환합니다.

이것을 호출하면 이미 완료된 프로세스에 "조인" 하는 부작용이 있습니다.

multiprocessing.cpu_count()
시스템의 CPU 수를 반환합니다.

이 숫자는 현재 프로세스에서 사용할 수 있는 CPU 수와 같지 않습니다. 사용 가능한 CPU 수는 len(os.sched_getaffinity(0)) 로 얻을 수 있습니다.

NotImplementedError를 일으킬 수 있습니다.

더 보기 os.cpu_count()
multiprocessing.current_process()
현재 프로세스에 해당하는 Process 객체를 반환합니다.

threading.current_thread()와 유사한 기능을 제공합니다.

multiprocessing.freeze_support()
multiprocessing을 사용하는 프로그램이 고정되어(frozen) 윈도우 실행 파일을 생성할 때를 위한 지원을 추가합니다. (py2exe, PyInstaller 및 cx_Freeze 에서 테스트 되었습니다.)

메인 모듈의 if __name__ == '__main__' 줄 바로 뒤에서 이 함수를 호출해야 합니다. 예를 들면:

from multiprocessing import Process, freeze_support

def f():
    print('hello world!')

if __name__ == '__main__':
    freeze_support()
    Process(target=f).start()
freeze_support() 줄이 생략된 경우 고정된 실행 파일을 실행하려고 하면 RuntimeError 가 발생합니다.

freeze_support() 호출은 윈도우가 아닌 다른 운영 체제에서 실행될 때는 아무런 영향을 미치지 않습니다. 또한, 모듈이 윈도우상의 파이썬 인터프리터에 의해 정상적으로 실행되는 경우 (프로그램이 고정되지 않은 경우)에도 freeze_support() 는 아무 효과가 없습니다.

multiprocessing.get_all_start_methods()
지원되는 시작 방법의 리스트를 반환하는데, 그 중 첫 번째가 기본값입니다. 가능한 시작 방법은 'fork', 'spawn' 및 'forkserver' 입니다. 윈도우에서는 'spawn' 만 사용할 수 있습니다. 유닉스에서는 'fork' 와 'spawn' 이 항상 지원되며 'fork' 가 기본값입니다.

버전 3.4에 추가.

multiprocessing.get_context(method=None)
multiprocessing 모듈과 같은 어트리뷰트를 가진 컨텍스트 객체를 반환합니다.

method 가 None 이면 기본 컨텍스트가 반환됩니다. 그렇지 않으면 method 는 'fork', 'spawn', 'forkserver' 이어야 합니다. 지정된 시작 방법을 사용할 수 없는 경우 ValueError 가 발생합니다.

버전 3.4에 추가.

multiprocessing.get_start_method(allow_none=False)
프로세스를 기동하기 위해서 사용되는 시작 방법의 이름을 돌려줍니다.

시작 방법이 고정되지 않았고 allow_none 이 거짓이면, 시작 방법이 기본값으로 고정되고 이름이 반환됩니다. 시작 방법이 고정되지 않았고 allow_none이 참이면, None 이 반환됩니다.

반환 값은 'fork', 'spawn', 'forkserver' 또는 None 입니다. 유닉스에서는 'fork' 가 기본값이고, 윈도우에서는 'spawn' 이 기본값입니다.

버전 3.4에 추가.

multiprocessing.set_executable()
자식 프로세스를 시작할 때 사용할 파이썬 인터프리터의 경로를 설정합니다. (기본적으로 sys.executable 이 사용됩니다). 파이썬은 내장하는 사람들은 아마도 다음과 같이 할 필요가 있습니다

set_executable(os.path.join(sys.exec_prefix, 'pythonw.exe'))
자식 프로세스를 만들기 전에 해야 합니다.

버전 3.4에서 변경: 이제 'spawn' 시작 방법을 사용할 때 유닉스에서 지원됩니다.

multiprocessing.set_start_method(method)
자식 프로세스를 시작하는 데 사용해야 하는 방법을 설정합니다. method 는 'fork', 'spawn' 또는 'forkserver' 일 수 있습니다.

이것은 한 번만 호출해야 하며, 메인 모듈의 if __name__ == '__main__' 절 내에서 보호되어야 합니다.

버전 3.4에 추가.

참고 multiprocessing 에는 threading.active_count(), threading.enumerate(), threading.settrace(), threading.setprofile(), threading.Timer 또는 threading.local 의 대응 물이 없습니다.

### Connection 객체

연결 객체를 사용하면 피클 가능한 객체나 문자열을 보내고 받을 수 있습니다. 메시지 지향 연결된 소켓으로 생각할 수 있습니다.

연결 객체는 보통 Pipe 를 사용해서 만들어집니다 -- 리스너와 클라이언트 도 참고하세요.

class multiprocessing.connection.Connection
send(obj)
연결의 반대편 끝에서 recv()를 사용하여 읽을 객체를 보냅니다.

객체는 피클 가능해야 합니다. 매우 큰 피클(약 32 MiB+, OS에 따라 다릅니다)은 ValueError 예외를 발생시킬 수 있습니다.

recv()
연결의 반대편 끝에서 send()로 보낸 객체를 반환합니다. 뭔가 수신할 때까지 블록합니다. 수신할 내용이 없고 반대편 끝이 닫혔으면 EOFError를 발생시킵니다.

fileno()
연결이 사용하는 파일 기술자나 핸들을 돌려줍니다.

close()
연결을 닫습니다.

연결이 가비지 수집될 때 자동으로 호출됩니다.

poll([timeout])
읽어 들일 데이터가 있는지를 돌려줍니다.

timeout 을 지정하지 않으면 즉시 반환됩니다. timeout 이 숫자면 블록할 최대 시간(초)을 지정합니다. timeout 이 None 이면 시간제한이 없습니다.

여러 개의 연결 객체를 multiprocessing.connection.wait() 을 사용하여 한 번에 폴링 할 수 있습니다.

send_bytes(buffer[, offset[, size]])
바이트열류 객체 의 바이트 데이터를 하나의 완전한 메시지로 보냅니다.

offset 이 주어지면 buffer 의 해당 위치부터 데이터를 읽습니다. size 가 주어지면 그만큼의 바이트를 버퍼에서 읽습니다. 매우 큰 버퍼(약 32 MiB+, OS에 따라 다릅니다)는 ValueError 예외를 발생시킬 수 있습니다

recv_bytes([maxlength])
접속의 반대편 끝에서 송신된 바이트 데이터의 완전한 메시지를 문자열로 돌려줍니다. 뭔가 수신할 때까지 블록합니다. 수신할 내용이 없고 반대편 끝이 닫혔으면 EOFError를 발생시킵니다.

maxlength 가 지정되고 메시지가 maxlength 보다 길면 OSError 가 발생하고 연결은 더는 읽을 수 없게 됩니다.

버전 3.3에서 변경: 이 함수는 IOError 를 발생시켜왔는데, 이제는 OSError 의 별칭입니다.

recv_bytes_into(buffer[, offset])
연결의 반대편 끝에서 보낸 바이트 데이터의 전체 메시지를 buffer 로 읽어 들이고, 메시지의 바이트 수를 반환합니다. 뭔가 수신할 때까지 블록합니다. 수신할 내용이 없고 반대편 끝이 닫혔으면 EOFError를 발생시킵니다.

buffer 는 쓰기 가능한 바이트열류 객체 여야 합니다. offset 이 지정되면, 버퍼의 그 위치로부터 메시지를 씁니다. offset은 buffer 길이보다 작은 음수가 아닌 정수여야 합니다 (바이트 단위).

버퍼가 너무 작으면 BufferTooShort 예외가 발생하고, 완전한 메시지는 e.args[0] 으로 제공되는데, 여기서 e 는 예외 인스턴스입니다.

버전 3.3에서 변경: 이제 연결 객체 자체를 Connection.send() 와 Connection.recv() 를 사용하여 프로세스 간에 전송할 수 있습니다.

버전 3.3에 추가: 이제 연결 객체는 컨텍스트 관리 프로토콜을 지원합니다 -- 컨텍스트 관리자 형를 보세요. __enter__() 는 연결 객체를 반환하고, __exit__() 는 close()를 호출합니다.

예를 들어:

>>> from multiprocessing import Pipe
>>> a, b = Pipe()
>>> a.send([1, 'hello', None])
>>> b.recv()
[1, 'hello', None]
>>> b.send_bytes(b'thank you')
>>> a.recv_bytes()
b'thank you'
>>> import array
>>> arr1 = array.array('i', range(5))
>>> arr2 = array.array('i', [0] * 10)
>>> a.send_bytes(arr1)
>>> count = b.recv_bytes_into(arr2)
>>> assert count == len(arr1) * arr1.itemsize
>>> arr2
array('i', [0, 1, 2, 3, 4, 0, 0, 0, 0, 0])
경고 Connection.recv() 메서드는 수신한 데이터를 자동으로 언 피클 합니다. 메시지를 보낸 프로세스를 신뢰할 수 없다면 보안상 위험 할 수 있습니다.
따라서, 연결 객체가 Pipe()를 사용하여 생성되지 않았다면, 일종의 인증을 수행한 후에만 recv() 및 send() 메서드를 사용해야 합니다. 인증 키를 참조하세요.

경고 프로세스가 파이프에 읽거나 쓰려고 할 때 죽으면, 파이프의 데이터가 손상될 가능성이 있습니다. 메시지 경계가 어디에 있는지 확신할 수 없는 상태가 될 가능성이 있기 때문입니다.

### 동기화 프리미티브

일반적으로 다중 프로세스 프로그램에서는 동기화 프리미티브가 다중 스레드 프로그램에서만큼 필요하지는 않습니다. threading 모듈에 대한 설명서를 참조하십시오.

관리자 객체를 사용하여 동기화 프리미티브를 생성할 수도 있습니다 -- 관리자를 참조하세요.

class multiprocessing.Barrier(parties[, action[, timeout]])
배리어(barrier) 객체: threading.Barrier 의 복제본.

버전 3.3에 추가.

class multiprocessing.BoundedSemaphore([value])
제한된 세마포어 객체: threading.BoundedSemaphore 과 유사한 대응 물.

대응 물과 한 가지 차이가 있습니다: acquire 메서드의 첫 번째 인자에 block 이라는 이름을 사용해서 Lock.acquire() 와의 일관성을 유지합니다.

참고 Mac OS X에서, sem_getvalue() 가 해당 플랫폼에 구현되어 있지 않기 때문에 Semaphore와 구별되지 않습니다.
class multiprocessing.Condition([lock])
조건 변수: threading.Condition 의 별칭.

lock 을 지정할 때는 multiprocessing 의 Lock 이나 RLock 객체여야 합니다.

버전 3.3에서 변경: wait_for() 메서드가 추가되었습니다.

class multiprocessing.Event
threading.Event 의 복제본.

class multiprocessing.Lock
비 재귀적 록 객체: threading.Lock 과 유사한 대응 물. 일단 프로세스 또는 스레드가 록을 획득하면, 프로세스 또는 스레드에서 록을 획득하려는 후속 시도는 록이 해제될 때까지 블록 됩니다; 모든 프로세스 또는 스레드가 이를 해제할 수 있습니다. 스레드에 적용되는 threading.Lock 의 개념과 동작은, 명시된 경우를 제외하고, multiprocessing.Lock 를 통해 프로세스나 스레드에 그대로 적용됩니다.

Lock 은 실제로 기본 컨텍스트로 초기화된 multiprocessing.synchronize.Lock 의 인스턴스를 반환하는 팩토리 함수입니다.

Lock 은 컨텍스트 관리자 프로토콜을 지원하므로 with 문에서 사용될 수 있습니다.

acquire(block=True, timeout=None)
블록하거나 블록하지 않는 방식으로 록을 획득합니다.

block 인자가 True (기본값) 로 설정되면, 메서드 호출은 록이 해제 상태가 될 때까지 블록 한 다음, 잠금 상태로 만들고 True 를 반환합니다. 이 첫 번째 인자의 이름은 threading.Lock.acquire() 와 다르다는 것에 유의하세요.

block 인자가 False 로 설정되면, 메서드 호출은 블록 되지 않습니다. 록이 현재 잠금 상태면 False 를 반환합니다. 그렇지 않으면 록을 잠금 상태로 설정하고 True 를 반환합니다.

timeout 에 대해 양의 부동 소수점 값을 사용하여 호출하는 경우, 록을 얻을 수 없는 한 최대 timeout 으로 지정된 시간(초) 동안 블록합니다. timeout 을 음수 값으로 호출하는 것은 timeout 에 0을 주는 것과 같습니다. timeout 값이 None (기본값) 인 호출은 제한 시간을 무한대로 설정합니다. timeout 에 대한 음수와 None 값의 처리는 threading.Lock.acquire() 에서 구현된 동작과 다르다는 것에 주의하십시오. timeout 인자는 block 인자가 False 로 설정되면 실제적인 의미는 없고 무시됩니다. 록이 획득되면 True 를 돌려주고, 제한 시간 초과가 발생하면 False 를 돌려줍니다.

release()
록을 해제합니다. 이것은 원래 록을 획득한 프로세스나 스레드뿐만 아니라 모든 프로세스나 스레드에서 호출 할 수 있습니다.

동작은 threading.Lock.release() 와 같지만, 해제된 록에서 호출될 때 ValueError 가 발생한다는 점만 다릅니다.

class multiprocessing.RLock
재귀적 록 객체: threading.RLock 과 유사한 대응 물. 재귀적 록은 획득한 프로세스 또는 스레드에 의해 해제되어야 합니다. 일단 프로세스나 스레드가 재귀적 록을 획득하면, 같은 프로세스나 스레드가 블록 없이 다시 획득할 수 있습니다; 해당 프로세스나 스레드는 획득할 때마다 한 번 해제해야 합니다.

RLock 은 실제로 기본 컨텍스트로 초기화된 multiprocessing.synchronize.RLock 의 인스턴스를 반환하는 팩토리 함수입니다.

RLock 은 컨텍스트 관리자 프로토콜을 지원하므로 with 문에서 사용될 수 있습니다.

acquire(block=True, timeout=None)
블록하거나 블록하지 않는 방식으로 록을 획득합니다.

block 인자를 True 로 설정해서 호출하면, 록이 현재 프로세스나 스레드가 이미 획득한 상태가 아니면 록이 (어떤 프로세스나 스레드도 획득하지 않은) 록 해제 상태가 될 때까지 블록합니다. 이후에 현재 프로세스나 스레드가 (소유권이 아직 없는 경우) 록 소유권을 얻게 되며 록 내 재귀 수준이 1 증가하고 True 를 반환합니다. 이 첫 번째 인자의 동작에는, 인자의 이름부터 시작해서 threading.RLock.acquire() 구현과 비교되는 몇 가지 차이점이 있습니다.

block 인자를 False 로 설정해서 호출하면 블록하지 않습니다. 록이 이미 다른 프로세스나 스레드에 의해 획득되었으면 (그래서 소유하고 있으면), 현재 프로세스나 스레드는 소유권을 갖지 않으며 록 내 재귀 수준은 변경되지 않고 False 를 반환합니다. 록이 해제 상태에 있으면, 현재 프로세스 또는 스레드가 소유권을 가져오며 재귀 수준이 증가하고 True 를 반환합니다.

timeout 인자의 사용법과 동작은 Lock.acquire() 와 같습니다. timeout 의 이러한 동작 중 일부는 threading.RLock.acquire() 에서 구현된 동작과 다르다는 것에 주의하십시오.

release()
재귀 수준을 감소시키면서 록을 해제합니다. 감소 후에 재귀 수준이 0이면, 록을 해제 상태(어떤 프로세스나 스레드에도 소유되지 않음)로 재설정하고, 다른 프로세스나 스레드가 록이 해제될 때까지 기다리며 블록하고 있는 경우 해당 프로세스나 스레드 중 정확히 하나가 계속 진행하도록 허용합니다. 감소 후에 재귀 수준이 여전히 0이 아닌 경우, 록은 획득된 상태로 남고 호출한 프로세스나 스레드에 의해 소유됩니다.

호출한 프로세스나 스레드가 록을 소유하고 있을 때만 이 메서드를 호출하십시오. 이 메서드가 소유자가 아닌 프로세스나 스레드에 의해 호출되거나, 록이 해제 (소유되지 않은) 상태면 AssertionError 가 발생합니다. 이 상황에서 발생하는 예외 형은 threading.RLock.release() 에서 구현된 동작과 다릅니다.

class multiprocessing.Semaphore([value])
세마포어 객체: threading.Semaphore 와 유사한 대응 물.

대응 물과 한 가지 차이가 있습니다: acquire 메서드의 첫 번째 인자에 block 이라는 이름을 사용해서 Lock.acquire() 와의 일관성을 유지합니다.

참고 Mac OS X에서, sem_timedwait 가 지원되지 않기 때문에, acquire() 를 시간제한 있게 호출하면 잠자는 루프를 사용하여 해당 함수의 동작을 흉내 냅니다.
참고 메인 스레드가 BoundedSemaphore.acquire(), Lock.acquire(), RLock.acquire(), Semaphore.acquire(), Condition.acquire() 또는 Condition.wait() 호출 때문에 블록 된 동안, Ctrl-C 에 의해 만들어진 SIGINT 시그널이 도착하면, 호출이 즉시 중단되고 KeyboardInterrupt 가 발생합니다.
이것은 threading 의 동작과는 다른데, SIGINT는 해당 블로킹 호출이 진행되는 동안 무시됩니다.

참고 이 패키지의 기능 중 일부는 호스트 운영 체제의 작동하는 공유 세마포어 구현을 요구합니다. 그런 것이 없으면, multiprocessing.synchronize 모듈이 비활성화되고, 임포트하려고 하면 ImportError 를 일으킵니다. 자세한 내용은 bpo-3770을 참조하십시오.

### 공유 ctypes 객체

자식 프로세스가 상속할 수 있는 공유 메모리를 사용하여 공유 객체를 만들 수 있습니다.

multiprocessing.Value(typecode_or_type, *args, lock=True)
공유 메모리에 할당된 ctypes 객체를 반환합니다. 기본적으로 반환 값은, 사실 객체에 대한 동기화 된 래퍼입니다. 객체 자체는 Value 의 value 어트리뷰트를 통해 접근 할 수 있습니다.

typecode_or_type 은 반환된 객체의 형을 결정합니다: ctypes 형이거나 array 모듈에 의해 사용되는 종류의 한 문자 typecode입니다. *args 는 형의 생성자로 전달됩니다.

lock 이 True (기본값) 면 값에 대한 액세스를 동기화하기 위해 새 재귀적 록 객체가 생성됩니다. lock 이 Lock 또는 RLock 객체인 경우, 이 값이 값에 대한 액세스를 동기화하는 데 사용됩니다. lock 이 False 면, 반환된 객체에 대한 액세스는 록에 의해 자동으로 보호되지 않으므로 "프로세스 안전" 하지 않습니다.

읽기와 쓰기를 포함하는 += 와 같은 연산은 원자 적(atomic)이지 않습니다. 따라서, 예를 들어, 공유 값을 원자 적으로 증가시키려면, 다음과 같이 하는 것으로는 충분하지 않습니다:

counter.value += 1
연관된 록이 재귀적이라고 가정하면 (기본적으로 그렇습니다), 대신 다음과 같이 할 수 있습니다

with counter.get_lock():
    counter.value += 1
lock 은 키워드 전용 인자입니다.

multiprocessing.Array(typecode_or_type, size_or_initializer, *, lock=True)
공유 메모리에서 할당된 ctypes 배열을 반환합니다. 기본적으로 반환 값은, 사실 배열에 대한 동기화 된 래퍼입니다.

typecode_or_type 은 반환된 배열의 요소의 형을 결정합니다: ctypes 형이거나 array 모듈에 의해 사용되는 종류의 한 문자 typecode입니다. size_or_initializer 가 정수면, 배열의 길이를 결정하고 배열은 0으로 초기화됩니다. 그렇지 않으면, size_or_initializer 는 배열을 초기화하는 데 사용되는 시퀀스고, 길이는 배열의 길이를 결정합니다.

lock 이 True (기본값) 면 값에 대한 액세스를 동기화하기 위해 새 록 객체가 생성됩니다. lock 이 Lock 또는 RLock 객체인 경우, 이 값이 값에 대한 액세스를 동기화하는 데 사용됩니다. lock 이 False 면, 반환된 객체에 대한 액세스는 록에 의해 자동으로 보호되지 않으므로 "프로세스 안전" 하지 않습니다.

lock 은 키워드 전용 인자입니다.

ctypes.c_char 의 배열은 value 와 raw 어트리뷰트를 가지고 있습니다. 이 어트리뷰트를 사용하여 문자열을 저장하고 꺼낼 수 있습니다.

multiprocessing.sharedctypes 모듈
multiprocessing.sharedctypes 모듈은 자식 프로세스에 의해 상속될 수 있는 공유 메모리에 ctypes 객체를 할당하는 기능을 제공합니다.

참고 공유 메모리에 포인터를 저장할 수는 있지만, 특정 프로세스의 주소 공간에 있는 위치를 참조하게 됩니다. 그러나 포인터는 두 번째 프로세스의 컨텍스트에서는 유효하지 않을 가능성이 커서, 두 번째 프로세스에서 포인터를 역 참조하려고 하면 충돌이 일어날 수 있습니다.
multiprocessing.sharedctypes.RawArray(typecode_or_type, size_or_initializer)
공유 메모리에 할당된 ctypes 배열을 반환합니다.

typecode_or_type 은 반환된 배열의 요소의 형을 결정합니다: ctypes 형이거나 array 모듈에 의해 사용되는 종류의 한 문자 typecode입니다. size_or_initializer 가 정수면, 배열의 길이를 결정하고 배열은 0으로 초기화됩니다. 그렇지 않으면, size_or_initializer 는 배열을 초기화하는 데 사용되는 시퀀스고, 길이는 배열의 길이를 결정합니다.

요소를 쓰고 읽는 것은 잠재적으로 원자 적이지 않습니다 -- 액세스가 록을 사용하여 자동으로 동기화되기 원하면 Array()를 대신 사용하세요.

multiprocessing.sharedctypes.RawValue(typecode_or_type, *args)
공유 메모리에 할당된 ctypes 객체를 반환합니다.

typecode_or_type 은 반환된 객체의 형을 결정합니다: ctypes 형이거나 array 모듈에 의해 사용되는 종류의 한 문자 typecode입니다. *args 는 형의 생성자로 전달됩니다.

값을 쓰고 읽는 것은 잠재적으로 원자 적이지 않습니다 -- 액세스가 록을 사용하여 자동으로 동기화되기 원하면 Value()를 대신 사용하세요.

ctypes.c_char 의 배열은 value 와 raw 어트리뷰트를 가지고 있습니다. 이 어트리뷰트를 사용하여 문자열을 저장하고 꺼낼 수 있습니다 -- ctypes 설명서를 보십시오.

multiprocessing.sharedctypes.Array(typecode_or_type, size_or_initializer, *, lock=True)
lock 값에 따라, 날 ctypes 배열 대신 프로세스 안전한 동기화 래퍼가 반환될 수 있다는 것을 제외하고는 RawArray() 와 같습니다.

lock 이 True (기본값) 면 값에 대한 액세스를 동기화하기 위해 새 록 객체가 생성됩니다. lock 이 Lock 또는 RLock 객체인 경우, 이 값이 값에 대한 액세스를 동기화하는 데 사용됩니다. lock 이 False 면, 반환된 객체에 대한 액세스는 록에 의해 자동으로 보호되지 않으므로 "프로세스 안전" 하지 않습니다.

lock 은 키워드 전용 인자입니다.

multiprocessing.sharedctypes.Value(typecode_or_type, *args, lock=True)
lock 값에 따라, 날 ctypes 객체 대신 프로세스 안전한 동기화 래퍼가 반환될 수 있다는 것을 제외하고는 RawValue() 와 같습니다.

lock 이 True (기본값) 면 값에 대한 액세스를 동기화하기 위해 새 록 객체가 생성됩니다. lock 이 Lock 또는 RLock 객체인 경우, 이 값이 값에 대한 액세스를 동기화하는 데 사용됩니다. lock 이 False 면, 반환된 객체에 대한 액세스는 록에 의해 자동으로 보호되지 않으므로 "프로세스 안전" 하지 않습니다.

lock 은 키워드 전용 인자입니다.

multiprocessing.sharedctypes.copy(obj)
공유 메모리에서 할당된 ctypes 객체를 반환합니다. 이 객체는 ctypes 객체 obj 의 복사본입니다.

multiprocessing.sharedctypes.synchronized(obj[, lock])
lock 을 사용하여 액세스를 동기화하는 ctypes 객체에 대한 프로세스 안전한 래퍼 객체를 반환합니다. lock 이 None (기본값)이면 multiprocessing.RLock 객체가 자동으로 생성됩니다.

동기화 래퍼는 래핑 된 객체의 메서드 외에도 두 개의 메서드를 더 갖습니다: get_obj() 는 래핑 된 객체를 반환하고, get_lock() 은 동기화에 사용되는 록 객체를 반환합니다.

래퍼를 통해 ctypes 객체에 액세스하는 것은, 날 ctypes 객체에 액세스하는 것보다 훨씬 느릴 수 있습니다.

버전 3.5에서 변경: 동기화된 객체는 컨텍스트 관리자 프로토콜을 지원합니다.

아래 표는 공유 메모리에 공유 ctypes 객체를 만드는 문법과 일반적인 ctypes 문법을 비교합니다. (표에서 MyStruct 는 ctypes.Structure 의 서브 클래스입니다.)

ctypes

type을 사용하는 공유 ctypes

typecode를 사용하는 공유 ctypes

c_double(2.4)

RawValue(c_double, 2.4)

RawValue('d', 2.4)

MyStruct(4, 6)

RawValue(MyStruct, 4, 6)

(c_short * 7)()

RawArray(c_short, 7)

RawArray('h', 7)

(c_int * 3)(9, 2, 8)

RawArray(c_int, (9, 2, 8))

RawArray('i', (9, 2, 8))

다음은 자식 프로세스가 여러 ctypes 객체를 수정하는 예입니다:

from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value, Array
from ctypes import Structure, c_double

class Point(Structure):
    _fields_ = [('x', c_double), ('y', c_double)]

def modify(n, x, s, A):
    n.value **= 2
    x.value **= 2
    s.value = s.value.upper()
    for a in A:
        a.x **= 2
        a.y **= 2

if __name__ == '__main__':
    lock = Lock()

    n = Value('i', 7)
    x = Value(c_double, 1.0/3.0, lock=False)
    s = Array('c', b'hello world', lock=lock)
    A = Array(Point, [(1.875,-6.25), (-5.75,2.0), (2.375,9.5)], lock=lock)

    p = Process(target=modify, args=(n, x, s, A))
    p.start()
    p.join()

    print(n.value)
    print(x.value)
    print(s.value)
    print([(a.x, a.y) for a in A])
인쇄되는 결과는 이렇습니다

49
0.1111111111111111
HELLO WORLD
[(3.515625, 39.0625), (33.0625, 4.0), (5.640625, 90.25)]

### 관리자

관리자는 서로 다른 컴퓨터에서 실행되는 프로세스 간에 네트워크를 통해 공유하는 것을 포함하여 서로 다른 프로세스 간에 공유할 수 있는 데이터를 만드는 방법을 제공합니다. 관리자 객체는 공유 객체 를 관리하는 서버 프로세스를 제어합니다. 다른 프로세스는 프락시를 사용하여 공유 객체에 액세스 할 수 있습니다.

multiprocessing.Manager()
프로세스 간에 객체를 공유하는 데 사용할 수 있는 시작된 SyncManager 객체를 반환합니다. 반환된 관리자 객체는 생성된 자식 프로세스에 해당하며 공유 객체를 만들고 해당 프락시를 반환하는 메서드가 있습니다.

관리자 프로세스는 가비지 수집되거나 상위 프로세스가 종료되자마자 종료됩니다. 관리자 클래스는 multiprocessing.managers 모듈에 정의되어 있습니다 :

class multiprocessing.managers.BaseManager([address[, authkey]])
BaseManager 객체를 만듭니다.

일단 생성되면 관리자 객체가 시작된 관리자 프로세스를 참조하게 하려고 start() 또는 get_server().serve_forever() 를 호출해야 합니다.

address 는 관리자 프로세스가 새 연결을 리슨하는 주소입니다. address 가 None 이면 임의의 것이 선택됩니다.

authkey 는 서버 프로세스로 들어오는 연결의 유효성을 검사하는 데 사용되는 인증 키입니다. authkey 가 None 이면 current_process().authkey 가 사용됩니다. 그렇지 않으면 authkey 가 사용되며 바이트열이어야 합니다.

start([initializer[, initargs]])
관리자를 시작시키기 위해 서브 프로세스를 시작합니다. initializer 가 None 이 아닌 경우, 서브 프로세스는 시작할 때 initializer(*initargs) 를 호출합니다.

get_server()
Manager의 제어를 받는 실제 서버를 나타내는 Server 객체를 반환합니다. Server 객체는 serve_forever() 메서드를 지원합니다:

>>>
>>> from multiprocessing.managers import BaseManager
>>> manager = BaseManager(address=('', 50000), authkey=b'abc')
>>> server = manager.get_server()
>>> server.serve_forever()
Server 는 추가로 address 어트리뷰트를 가지고 있습니다.

connect()
지역 관리자 객체를 원격 관리자 프로세스에 연결합니다:

>>>
>>> from multiprocessing.managers import BaseManager
>>> m = BaseManager(address=('127.0.0.1', 50000), authkey=b'abc')
>>> m.connect()
shutdown()
관리자가 사용하는 프로세스를 중지합니다. start()를 사용하여 서버 프로세스를 시작한 경우에만 사용할 수 있습니다.

여러 번 호출 될 수 있습니다.

register(typeid[, callable[, proxytype[, exposed[, method_to_typeid[, create_method]]]]])
관리자 클래스에 형이나 콜러블을 등록하는데 사용할 수 있는 클래스 메서드.

typeid 는 특정 형의 공유 객체를 식별하는 데 사용되는 "형 식별자" 입니다. 문자열이어야 합니다.

callable 은 이 형 식별자에 대한 객체를 만드는 데 사용되는 콜러블 객체입니다. 관리자 인스턴스가 connect() 메서드를 사용하여 서버에 연결되거나, create_method 인자가 False 면 None 으로 남겨 둘 수 있습니다.

proxytype 은, 이 typeid 의 공유 객체의 프락시를 만드는 데 사용되는 BaseProxy 의 서브 클래스입니다. None 이면 프락시 클래스가 자동으로 생성됩니다.

exposed 는 이 typeid에 대한 프락시가 BaseProxy._callmethod() 를 사용하여 액세스 할 수 있도록 허용해야 하는 메서드 이름의 시퀀스를 지정하는 데 사용됩니다. (만약 exposed 가 None 이면, 존재하는 경우, proxytype._exposed_ 가 대신 사용됩니다.) exposed 리스트가 지정되지 않은 경우, 공유 객체의 모든 "공용 메서드" 에 액세스 할 수 있습니다. (여기서 "공용 메서드" 는 __call__() 메서드가 있고 그 이름이 '_' 로 시작하지 않는 어트리뷰트를 의미합니다.)

method_to_typeid 는 프락시를 반환해야 하는 노출된 메서드의 반환형을 지정하는 데 사용되는 매핑입니다. 메서드 이름을 typeid 문자열로 매핑합니다. (만일 method_to_typeid 가 None 이면, 존재한다면, proxytype._method_to_typeid_ 가 대신 사용됩니다.) 메서드의 이름이 이 매핑의 키가 아니거나 매핑이 None 이면, 메서드에 의해 반환된 객체는 값으로 복사됩니다.

create_method 는 이름이 typeid 인 메서드를 만들어야 하는지를 결정합니다. 이 메서드는 서버 프로세스에 새 공유 객체를 만들고 프락시를 반환하도록 지시하는 데 사용될 수 있습니다. 기본적으로 True 입니다.

BaseManager 인스턴스는 읽기 전용 프로퍼티를 하나 가지고 있습니다:

address
관리자가 사용하는 주소.

버전 3.3에서 변경: 관리자 객체는 컨텍스트 관리 프로토콜을 지원합니다 -- 컨텍스트 관리자 형를 보세요. __enter__() 는 서버 프로세스를 시작하고 (아직 시작하지 않았다면), 관리자 객체를 반환합니다. __exit__() 는 shutdown()을 호출합니다.

이전 버전에서 __enter__() 는 관리자의 서버 프로세스가 아직 시작되지 않았을 때 시작시키지 않았습니다.

class multiprocessing.managers.SyncManager
프로세스의 동기화에 사용할 수 있는 BaseManager 의 서브 클래스입니다. 이 형의 객체는 multiprocessing.Manager() 에 의해 반환됩니다.

이 클래스의 메서드는 여러 프로세스에서 동기화 할 수 있도록 일반적으로 사용되는 많은 데이터형을 생성하고 프락시 객체를 반환합니다. 특히 공유 리스트와 딕셔너리가 포함됩니다.

Barrier(parties[, action[, timeout]])
공유 threading.Barrier 객체를 생성하고 프락시를 반환합니다.

버전 3.3에 추가.

BoundedSemaphore([value])
공유 threading.BoundedSemaphore 객체를 생성하고 프락시를 반환합니다.

Condition([lock])
공유 threading.Condition 객체를 생성하고 프락시를 반환합니다.

lock 이 제공되면 threading.Lock 또는 threading.RLock 객체에 대한 프락시여야 합니다.

버전 3.3에서 변경: wait_for() 메서드가 추가되었습니다.

Event()
공유 threading.Event 객체를 생성하고 프락시를 반환합니다.

Lock()
공유 threading.Lock 객체를 생성하고 프락시를 반환합니다.

Namespace()
공유 Namespace 객체를 생성하고 프락시를 반환합니다.

Queue([maxsize])
공유 queue.Queue 객체를 생성하고 프락시를 반환합니다.

RLock()
공유 threading.RLock 객체를 생성하고 프락시를 반환합니다.

Semaphore([value])
공유 threading.Semaphore 객체를 생성하고 프락시를 반환합니다.

Array(typecode, sequence)
배열을 만들고 프락시를 반환합니다.

Value(typecode, value)
쓰기 가능한 value 어트리뷰트를 가진 객체를 생성하고 프락시를 반환합니다.

dict()
dict(mapping)
dict(sequence)
공유 dict 객체를 생성하고 프락시를 반환합니다.

list()
list(sequence)
공유 list 객체를 생성하고 프락시를 반환합니다.

버전 3.6에서 변경: 공유 객체는 중첩될 수 있습니다. 예를 들어, 공유 리스트와 같은 공유 컨테이너 객체는, SyncManager 에 의해 모두 관리되고 동기화되는 다른 공유 객체를 포함 할 수 있습니다.

class multiprocessing.managers.Namespace
SyncManager 로 등록 할 수 있는 형입니다.

이름 공간 객체에는 공용 메서드가 없지만, 쓰기 가능한 어트리뷰트가 있습니다. repr 은 그것의 어트리뷰트 값을 보여줍니다.

그러나, 이름 공간 객체의 프락시를 사용할 때, '_' 로 시작하는 어트리뷰트는 프락시의 어트리뷰트가 되며 참조 대상의 어트리뷰트가 아닙니다:

>>> manager = multiprocessing.Manager()
>>> Global = manager.Namespace()
>>> Global.x = 10
>>> Global.y = 'hello'
>>> Global._z = 12.3    # this is an attribute of the proxy
>>> print(Global)
Namespace(x=10, y='hello')
사용자 정의 관리자
자신만의 관리자를 만들려면, BaseManager 의 서브 클래스를 만들고 register() 클래스 메서드를 사용하여 새로운 형이나 콜러블을 관리자 클래스에 등록합니다. 예를 들면:

from multiprocessing.managers import BaseManager

class MathsClass:
    def add(self, x, y):
        return x + y
    def mul(self, x, y):
        return x * y

class MyManager(BaseManager):
    pass

MyManager.register('Maths', MathsClass)

if __name__ == '__main__':
    with MyManager() as manager:
        maths = manager.Maths()
        print(maths.add(4, 3))         # prints 7
        print(maths.mul(7, 8))         # prints 56
원격 관리자 사용하기
한 기계에서 관리자 서버를 실행하고 다른 기계의 클라이언트가 관리자 서버를 사용하도록 할 수 있습니다 (관련된 방화벽이 허용한다고 가정합니다).

다음 명령을 실행하면 원격 클라이언트가 액세스 할 수 있는 단일 공유 큐를 위한 서버가 만들어집니다:

>>>
>>> from multiprocessing.managers import BaseManager
>>> from queue import Queue
>>> queue = Queue()
>>> class QueueManager(BaseManager): pass
>>> QueueManager.register('get_queue', callable=lambda:queue)
>>> m = QueueManager(address=('', 50000), authkey=b'abracadabra')
>>> s = m.get_server()
>>> s.serve_forever()
한 클라이언트는 다음과 같이 서버에 액세스 할 수 있습니다:

>>>
>>> from multiprocessing.managers import BaseManager
>>> class QueueManager(BaseManager): pass
>>> QueueManager.register('get_queue')
>>> m = QueueManager(address=('foo.bar.org', 50000), authkey=b'abracadabra')
>>> m.connect()
>>> queue = m.get_queue()
>>> queue.put('hello')
또 다른 클라이언트도 사용할 수 있습니다:

>>>
>>> from multiprocessing.managers import BaseManager
>>> class QueueManager(BaseManager): pass
>>> QueueManager.register('get_queue')
>>> m = QueueManager(address=('foo.bar.org', 50000), authkey=b'abracadabra')
>>> m.connect()
>>> queue = m.get_queue()
>>> queue.get()
'hello'
지역 프로세스 역시, 위의 클라이언트가 원격으로 액세스하는 코드를 사용하여 같은 큐에 액세스 할 수 있습니다:

>>>
>>> from multiprocessing import Process, Queue
>>> from multiprocessing.managers import BaseManager
>>> class Worker(Process):
...     def __init__(self, q):
...         self.q = q
...         super(Worker, self).__init__()
...     def run(self):
...         self.q.put('local hello')
...
>>> queue = Queue()
>>> w = Worker(queue)
>>> w.start()
>>> class QueueManager(BaseManager): pass
...
>>> QueueManager.register('get_queue', callable=lambda: queue)
>>> m = QueueManager(address=('', 50000), authkey=b'abracadabra')
>>> s = m.get_server()
>>> s.serve_forever()

### 프락시 객체

프락시는 (아마도) 다른 프로세스에 있는 공유 객체를 가리키는 객체입니다. 공유 객체는 프락시의 지시 대상 이라고 합니다. 여러 프락시 객체는 같은 지시 대상을 가질 수 있습니다.

프락시 객체에는 지시 대상의 해당 메서드를 호출하는 메서드가 있습니다 (그러나 지시 대상의 모든 메서드가 반드시 프락시를 통해 사용할 수 있는 것은 아닙니다). 이런 식으로, 프락시는 지시 대상처럼 사용될 수 있습니다:

>>> from multiprocessing import Manager
>>> manager = Manager()
>>> l = manager.list([i*i for i in range(10)])
>>> print(l)
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
>>> print(repr(l))
<ListProxy object, typeid 'list' at 0x...>
>>> l[4]
16
>>> l[2:5]
[4, 9, 16]
프락시에 str() 을 적용하면 지시 대상의 표현이 반환되는 반면, repr() 을 적용하면 프락시의 표현이 반환됩니다.

프락시 객체의 중요한 특징은, 피클 가능해서 프로세스 간에 전달될 수 있다는 것입니다. 지시 대상은 프락시 객체를 포함 할 수 있습니다. 이것은 관리된 리스트, 딕셔너리 및 다른 프락시 객체 의 중첩을 허용합니다:

>>> a = manager.list()
>>> b = manager.list()
>>> a.append(b)         # referent of a now contains referent of b
>>> print(a, b)
[<ListProxy object, typeid 'list' at ...>] []
>>> b.append('hello')
>>> print(a[0], b)
['hello'] ['hello']
비슷하게, 딕셔너리와 리스트 프락시는 서로 중첩될 수 있습니다:

>>>
>>> l_outer = manager.list([ manager.dict() for i in range(2) ])
>>> d_first_inner = l_outer[0]
>>> d_first_inner['a'] = 1
>>> d_first_inner['b'] = 2
>>> l_outer[1]['c'] = 3
>>> l_outer[1]['z'] = 26
>>> print(l_outer[0])
{'a': 1, 'b': 2}
>>> print(l_outer[1])
{'c': 3, 'z': 26}
(프락시가 아닌) 표준 list 또는 dict 객체가 지시 대상에 포함되어있는 경우, 이 가변 값들에 대한 수정은 관리자를 통해 전파되지 않습니다. 포함된 값이 언제 수정되는지 프락시가 알 방법이 없기 때문입니다. 그러나 컨테이너 프락시에 값을 저장하는 것(프락시 객체의 __setitem__ 을 호출합니다)은 관리자를 통해 전파되므로, 그 항목을 효과적으로 수정하기 위해, 수정된 값을 컨테이너 프락시에 다시 대입할 수 있습니다:

# create a list proxy and append a mutable object (a dictionary)
lproxy = manager.list()
lproxy.append({})
# now mutate the dictionary
d = lproxy[0]
d['a'] = 1
d['b'] = 2
# at this point, the changes to d are not yet synced, but by
# updating the dictionary, the proxy is notified of the change
lproxy[0] = d
이 접근법은 아마도 대부분의 사용 사례에서 중첩된 프락시 객체를 사용하는 것보다 불편하지만, 동기화에 대한 제어 수준을 보여줍니다.

참고 multiprocessing 의 프락시 형은 값으로 비교하는 것을 지원하지 않습니다. 그래서, 예를 들어, 이런 결과를 얻습니다:
>>> manager.list([1,2,3]) == [1,2,3]
False
비교할 때는 지시 대상의 사본을 대신 사용해야 합니다.

class multiprocessing.managers.BaseProxy
프락시 객체는 BaseProxy 의 서브 클래스의 인스턴스입니다.

_callmethod(methodname[, args[, kwds]])
프락시의 지시 대상 메서드를 호출하고 결과를 반환합니다.

proxy 가 프락시이고, 그 지시 대상이 obj 면, 표현식

proxy._callmethod(methodname, args, kwds)
은 표현식

getattr(obj, methodname)(*args, **kwds)
을 관리자 프로세스에서 평가합니다.

반환된 값은 호출 결과의 복사본이거나 새 공유 객체에 대한 프락시입니다 -- BaseManager.register() 의 method_to_typeid 인자에 대한 설명서를 보십시오.

호출 때문에 예외가 발생하면, _callmethod() 가 다시 일으킵니다. 관리자 프로세스에서 다른 예외가 발생하면 RemoteError 예외로 변환되어 _callmethod() 가 일으킵니다.

특히, methodname 이 노출되지 않았으면 예외가 발생합니다.

_callmethod() 사용법의 예:

>>> l = manager.list(range(10))
>>> l._callmethod('__len__')
10
>>> l._callmethod('__getitem__', (slice(2, 7),)) # equivalent to l[2:7]
[2, 3, 4, 5, 6]
>>> l._callmethod('__getitem__', (20,))          # equivalent to l[20]
Traceback (most recent call last):
...
IndexError: list index out of range
_getvalue()
지시 대상의 복사본을 반환합니다.

지시 대상이 피클 가능하지 않으면 예외가 발생합니다.

__repr__()
프락시 객체의 표현을 반환합니다.

__str__()
지시 대상의 표현을 반환합니다.

정리
프락시 객체는 weakref 콜백을 사용해서 가비지 수집 시 자신의 지시 대상을 소유한 관리자에서 자신을 등록 취소합니다.

더는 참조하는 프락시가 없는 경우 공유 객체는 관리자 프로세스에서 삭제됩니다.

### 프로세스 풀

Pool 클래스를 사용하여, 제출된 작업을 수행할 프로세스 풀을 만들 수 있습니다.

class multiprocessing.pool.Pool([processes[, initializer[, initargs[, maxtasksperchild[, context]]]]])
작업을 제출할 수 있는 작업자 프로세스 풀을 제어하는 프로세스 풀 객체. 제한 시간과 콜백을 사용하는 비동기 결과를 지원하고 병렬 map 구현을 제공합니다.

processes 는 사용할 작업자 프로세스 수입니다. processes 가 None 이면 os.cpu_count() 에 의해 반환되는 수가 사용됩니다.

initializer 가 None 이 아니면, 각 작업자 프로세스는 시작할 때 initializer(*initargs) 를 호출합니다.

maxtasksperchild 는, 사용되지 않는 자원을 해제할 수 있도록, 작업 프로세스가 종료되고 새 작업 프로세스로 교체되기 전에 완료할 수 있는 작업 수입니다. 기본 maxtasksperchild 는 None 입니다. 이는 작업자 프로세스가 풀만큼 오래감을 의미합니다.

context 는 작업자 프로세스를 시작하는 데 사용되는 컨텍스트를 지정하는 데 사용할 수 있습니다. 보통 풀은 multiprocessing.Pool() 또는 컨텍스트 객체의 Pool() 메서드를 사용하여 생성됩니다. 두 경우 모두 context 가 적절하게 설정됩니다.

풀 객체의 메서드는 풀을 생성한 프로세스에 의해서만 호출되어야 합니다.

버전 3.2에 추가: maxtasksperchild

버전 3.4에 추가: context

참고 Pool 내의 작업자 프로세스는 일반적으로 Pool의 작업 큐의 전체 지속 기간 지속합니다. 작업자가 잡은 자원을 해제하기 위해 다른 시스템 (가령 Apache, mod_wsgi 등)에서 흔히 사용되는 패턴은, 풀 내에 있는 작업자가 종료되고 새 프로세스가 스폰 되어 예전 것을 교체하기 전에 일정한 분량의 작업만 완료하도록 하는 것입니다. Pool 의 maxtasksperchild 인자는 이 기능을 일반 사용자에게 노출합니다.
apply(func[, args[, kwds]])
인자 args 및 키워드 인자 kwds 를 사용하여 func 를 호출합니다. 결과가 준비될 때까지 블록 됩니다. 이 블록 때문에, apply_async() 가 병렬로 작업을 수행하는 데 더 적합합니다. 또한 func 는 풀의 작업자 중 하나에서만 실행됩니다.

apply_async(func[, args[, kwds[, callback[, error_callback]]]])
결과 객체를 반환하는 apply() 메서드의 변형입니다.

callback 이 지정되면 단일 인자를 받아들이는 콜러블이어야 합니다. 결과가 준비되면 callback 을 이 결과를 인자로 호출합니다. 실패한 결과면 error_callback 이 대신 적용됩니다.

error_callback 이 지정되면 단일 인자를 허용하는 콜러블이어야 합니다. 대상 함수가 실패하면, error_callback 이 예외 인스턴스를 인자로 호출됩니다.

콜백은 즉시 완료되어야 합니다. 그렇지 않으면 결과를 처리하는 스레드가 블록 됩니다.

map(func, iterable[, chunksize])
map() 내장 함수의 병렬 버전입니다 (하지만 하나의 iterable 인자만 지원합니다). 결과가 준비될 때까지 블록 됩니다.

이 메서드는 iterable을 여러 묶음으로 잘라서 별도의 작업으로 프로세스 풀에 제출합니다. 이러한 묶음의 (대략적인) 크기는 chunksize 를 양의 정수로 설정하여 지정할 수 있습니다.

매우 긴 이터러블은 높은 메모리 사용을 유발할 수 있습니다. 더 나은 효율성을 위해, 명시적인 chunksize 옵션으로 imap()이나 imap_unordered()를 사용하는 것을 고려하십시오.

map_async(func, iterable[, chunksize[, callback[, error_callback]]])
결과 객체를 반환하는 map() 메서드의 변형입니다.

callback 이 지정되면 단일 인자를 받아들이는 콜러블이어야 합니다. 결과가 준비되면 callback 을 이 결과를 인자로 호출합니다. 실패한 결과면 error_callback 이 대신 적용됩니다.

error_callback 이 지정되면 단일 인자를 허용하는 콜러블이어야 합니다. 대상 함수가 실패하면, error_callback 이 예외 인스턴스를 인자로 호출됩니다.

콜백은 즉시 완료되어야 합니다. 그렇지 않으면 결과를 처리하는 스레드가 블록 됩니다.

imap(func, iterable[, chunksize])
map() 의 느긋한 버전.

chunksize 인자는 map() 메서드에서 사용된 인자와 같습니다. 매우 긴 iterable의 경우 chunksize 에 큰 값을 사용하면 기본값 1 을 사용하는 것보다 작업을 많이 빠르게 완료 할 수 있습니다.

또한 chunksize 가 1 이면 imap() 메서드에 의해 반환된 이터레이터의 next() 메서드는 선택적 timeout 매개 변수를 가집니다: next(timeout) 은 결과가 timeout 초 내에 반환될 수 없는 경우 multiprocessing.TimeoutError 를 발생시킵니다.

imap_unordered(func, iterable[, chunksize])
imap()과 같지만, 반환된 이터레이터가 제공하는 결과의 순서가 임의적인 것으로 간주하여야 합니다. (단 하나의 작업자 프로세스가 있는 경우에만 순서가 "올바름" 이 보장됩니다.

starmap(func, iterable[, chunksize])
map()과 같지만, iterable 의 요소가 인자로 언팩 될 이터러블일 것으로 기대합니다.

따라서 iterable 이 [(1,2), (3, 4)] 미면 결과는 [func(1,2), func(3,4)] 가 됩니다.

버전 3.3에 추가.

starmap_async(func, iterable[, chunksize[, callback[, error_callback]]])
starmap() 과 map_async() 의 조합으로 이터러블의 iterable 을 이터레이트하고 이터러블을 언팩해서 func 를 호출합니다. 결과 객체를 반환합니다.

버전 3.3에 추가.

close()
더는 작업이 풀에 제출되지 않도록 합니다. 모든 작업이 완료되면 작업자 프로세스가 종료됩니다.

terminate()
계류 중인 작업을 완료하지 않고 즉시 작업자 프로세스를 중지합니다. 풀 객체가 가비지 수집될 때 terminate() 가 즉시 호출됩니다.

join()
작업자 프로세스가 종료될 때까지 기다립니다. join() 호출 전에 반드시 close() 나 terminate()를 호출해야합니다 .

버전 3.3에 추가: 풀 객체는 이제 컨텍스트 관리 프로토콜을 지원합니다 -- 컨텍스트 관리자 형를 보십시오. __enter__() 는 풀 객체를 반환하고, __exit__() 는 terminate()를 호출합니다.

class multiprocessing.pool.AsyncResult
Pool.apply_async()와 Pool.map_async() 에 의해 반환되는 결과의 클래스.

get([timeout])
결과가 도착할 때 반환합니다. timeout 이 None 이 아니고 결과가 timeout 초 내에 도착하지 않으면 multiprocessing.TimeoutError 가 발생합니다. 원격 호출이 예외를 발생시키는 경우 해당 예외는 get() 에 의해 다시 발생합니다.

wait([timeout])
결과가 사용 가능할 때까지 또는 timeout 초가 지날 때까지 기다립니다.

ready()
호출이 완료했는지를 돌려줍니다.

successful()
예외를 발생시키지 않고 호출이 완료되었는지를 돌려줍니다. 결과가 준비되지 않았으면 AssertionError 를 발생시킵니다.

다음 예제는 풀 사용 방법을 보여줍니다.:

from multiprocessing import Pool
import time

def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(processes=4) as pool:         # start 4 worker processes
        result = pool.apply_async(f, (10,)) # evaluate "f(10)" asynchronously in a single process
        print(result.get(timeout=1))        # prints "100" unless your computer is *very* slow

        print(pool.map(f, range(10)))       # prints "[0, 1, 4,..., 81]"

        it = pool.imap(f, range(10))
        print(next(it))                     # prints "0"
        print(next(it))                     # prints "1"
        print(it.next(timeout=1))           # prints "4" unless your computer is *very* slow

        result = pool.apply_async(time.sleep, (10,))
        print(result.get(timeout=1))        # raises multiprocessing.TimeoutError

### 리스너와 클라이언트

보통 프로세스 간 메시지 전달은 큐를 사용하거나 Pipe() 가 반환하는 Connection 객체를 사용하여 수행됩니다.

그러나, multiprocessing.connection 모듈은 약간의 추가적인 유연성을 허용합니다. 기본적으로 소켓이나 윈도우의 이름있는 파이프를 다루는 높은 수준의 메시지 지향 API를 제공합니다. 또한 hmac 모듈을 사용한 다이제스트 인증 과 다중 연결을 동시에 폴링하는 방법을 지원합니다.

multiprocessing.connection.deliver_challenge(connection, authkey)
무작위로 생성된 메시지를 연결의 다른 쪽 끝으로 보내고 응답을 기다립니다.

응답이 authkey 를 키로 사용하는 메시지의 다이제스트와 일치하면 환영 메시지가 연결의 다른 끝으로 전송됩니다. 그렇지 않으면 AuthenticationError 가 발생합니다.

multiprocessing.connection.answer_challenge(connection, authkey)
메시지를 수신하고, authkey 를 키로 사용하여 메시지의 다이제스트를 계산한 다음, 다이제스트를 다시 보냅니다.

환영 메시지가 수신되지 않으면, AuthenticationError 가 발생합니다.

multiprocessing.connection.Client(address[, family[, authkey]])
주소 address 를 사용하는 리스너에 대한 연결을 설정하려고 시도하고, Connection을 반환합니다.

연결 유형은 family 인자에 의해 결정되지만, 일반적으로 address 형식에서 유추 할 수 있으므로 일반적으로 생략 할 수 있습니다. (주소 형식를 참조하세요)

authkey 가 주어지고 None이 아니라면, 바이트열이어야 하며 HMAC 기반 인증 챌린지의 비밀 키로 사용됩니다. authkey 가 None이면, 인증이 수행되지 않습니다. 인증이 실패하면 AuthenticationError 가 발생합니다. 인증 키를 보세요.

class multiprocessing.connection.Listener([address[, family[, backlog[, authkey]]]])
연결을 '리스닝' 하는 바인드된 소켓이나 윈도우의 이름있는 파이프에 대한 래퍼입니다.

address 는 리스너 객체의 바인드된 소켓이나 이름있는 파이프가 사용할 주소입니다.

참고 주소가 '0.0.0.0' 인 경우, 주소는 윈도우에서 연결 가능한 끝점이 아닙니다. 연결할 수 있는 끝점이 필요한 경우, '127.0.0.1'을 사용해야 합니다.
family 는 사용할 소켓(또는 이름있는 파이프)의 유형입니다. 문자열 'AF_INET' (TCP 소켓), 'AF_UNIX' (유닉스 도메인 소켓), 'AF_PIPE' (윈도우 이름있는 파이프) 중 하나일 수 있습니다. 이 중 오직 첫 번째 것만 항상 사용할 수 있음이 보장됩니다. family 가 None 이면, address 의 형식으로부터 유추됩니다. address 역시 None 이면, 기본값이 선택됩니다. 이 기본값은 사용 가능한 것 중 가장 빠른 것으로 기대되는 것입니다. 주소 형식를 참조하세요. family 가 'AF_UNIX' 이고 주소가 None 이면, 소켓은 tempfile.mkstemp() 를 사용하여 만들어진 비공개 임시 디렉터리에 생성됩니다.

리스너 객체가 소켓을 사용하면, backlog (기본적으로 1) 는 소켓이 바인드되면 소켓의 listen() 메서드에 전달됩니다.

authkey 가 주어지고 None이 아니라면, 바이트열이어야 하며 HMAC 기반 인증 챌린지의 비밀 키로 사용됩니다. authkey 가 None이면, 인증이 수행되지 않습니다. 인증이 실패하면 AuthenticationError 가 발생합니다. 인증 키를 보세요.

accept()
리스너 객체의 바인드된 소켓 또는 이름있는 파이프에 대한 연결을 수락하고 Connection 객체를 반환합니다. 인증이 시도되고 실패하면 AuthenticationError 가 발생합니다.

close()
리스너 객체의 바운드된 소켓 또는 이름있는 파이프를 닫습니다. 리스너가 가비지 수집될 때 자동으로 호출됩니다. 그러나 명시적으로 호출하는 것이 좋습니다.

리스너 객체는 다음과 같은 읽기 전용 프로퍼티를 가집니다:

address
리스너 객체에서 사용 중인 주소.

last_accepted
마지막으로 수락한 연결이 온 주소. 없으면 None 입니다.

버전 3.3에 추가: 리스너 객체는 컨텍스트 관리 프로토콜을 지원합니다 -- 컨텍스트 관리자 형를 보세요. __enter__() 는 리스너 객체를 반환하고, __exit__() 는 close()를 호출합니다.

multiprocessing.connection.wait(object_list, timeout=None)
object_list 에 있는 객체가 준비될 때까지 기다립니다. object_list 에 있는 객체 중 준비된 것들의 리스트를 반환합니다. timeout 이 float면, 호출이 최대 지정된 초만큼 블록 됩니다. timeout 이 None 이면, 시간제한 없이 블록 됩니다. 음수 timeout은 0과 같습니다.

유닉스와 윈도우에서 모두, object_list 에 등장할 수 있는 객체는 다음과 같습니다.

읽기 가능한 Connection 객체;

연결되고 읽기 가능한 socket.socket 객체; 또는

Process 객체의 sentinel 어트리뷰트.

연결이나 소켓 객체는 읽을 수 있는 데이터가 있거나 반대편 끝이 닫히면 준비가 됩니다.

유닉스: wait(object_list, timeout) 은 select.select(object_list, [], [], timeout)과 거의 동등합니다. 차이점은, select.select() 가 시그널에 의해 인터럽트 되면, 에러 번호 EINTR 로 OSError 를 일으키지만, wait() 는 예외를 일으키지 않는다는 것입니다.

윈도우: object_list 의 항목은 (Win32 함수 WaitForMultipleObjects() 의 설명서에서 사용된 정의에 따라) 대기 가능한 정수 핸들이거나, 소켓 핸들이나 파이프 핸들을 반환하는 fileno() 메서드가 있는 개체입니다. (파이프 핸들과 소켓 핸들은 대기 가능한 핸들이 아님 에 유의하십시오.)

버전 3.3에 추가.

예제

다음 서버 코드는 인증 키로 'secret password' 를 사용하는 리스너를 만듭니다. 그런 다음 연결을 기다리고 어떤 데이터를 클라이언트로 보냅니다.:

from multiprocessing.connection import Listener
from array import array

address = ('localhost', 6000)     # family is deduced to be 'AF_INET'

with Listener(address, authkey=b'secret password') as listener:
    with listener.accept() as conn:
        print('connection accepted from', listener.last_accepted)

        conn.send([2.25, None, 'junk', float])

        conn.send_bytes(b'hello')

        conn.send_bytes(array('i', [42, 1729]))
다음 코드는 서버에 연결하고 서버로부터 어떤 데이터를 받습니다:

from multiprocessing.connection import Client
from array import array

address = ('localhost', 6000)

with Client(address, authkey=b'secret password') as conn:
    print(conn.recv())                  # => [2.25, None, 'junk', float]

    print(conn.recv_bytes())            # => 'hello'

    arr = array('i', [0, 0, 0, 0, 0])
    print(conn.recv_bytes_into(arr))    # => 8
    print(arr)                          # => array('i', [42, 1729, 0, 0, 0])
다음 코드는 wait() 을 사용하여 여러 프로세스로부터 오는 메시지를 한 번에 기다립니다:

import time, random
from multiprocessing import Process, Pipe, current_process
from multiprocessing.connection import wait

def foo(w):
    for i in range(10):
        w.send((i, current_process().name))
    w.close()

if __name__ == '__main__':
    readers = []

    for i in range(4):
        r, w = Pipe(duplex=False)
        readers.append(r)
        p = Process(target=foo, args=(w,))
        p.start()
        # We close the writable end of the pipe now to be sure that
        # p is the only process which owns a handle for it.  This
        # ensures that when p closes its handle for the writable end,
        # wait() will promptly report the readable end as being ready.
        w.close()

    while readers:
        for r in wait(readers):
            try:
                msg = r.recv()
            except EOFError:
                readers.remove(r)
            else:
                print(msg)
주소 형식
'AF_INET' 주소는 (hostname, port) 형식의 튜플입니다. hostname 은 문자열이고, port 는 정수입니다.

'AF_UNIX' 주소는 파일 시스템의 파일 이름을 나타내는 문자열입니다.

'AF_PIPE' 주소는 형식
r'\.\pipe{PipeName}' 의 문자열입니다. Client() 를 사용하여 ServerName 이라는 원격 컴퓨터의 이름있는 파이프에 연결하려면, 대신 r'\ServerName\pipe{PipeName}' 형식의 주소를 사용해야 합니다.

두 개의 역 슬래시로 시작하는 문자열은 기본적으로 'AF_UNIX' 주소가 아니라 'AF_PIPE' 주소로 간주합니다.

### 인증 키

Connection.recv 를 사용할 때, 수신된 데이터는 자동으로 언 피클 됩니다. 안타깝게도, 신뢰할 수 없는 출처의 데이터를 언 피클 하는 것은 보안상의 위험입니다. 때문에 Listener와 Client() 는 hmac 모듈을 사용하여 다이제스트 인증을 제공합니다.

인증 키는 암호로 여겨질 수 있는 바이트열입니다: 일단 연결이 이루어지면 양 끝은 다른 쪽이 인증 키를 알고 있음을 증명하도록 요구합니다. (양쪽 끝이 같은 키를 사용하고 있음을 증명하는 데는 연결을 통해 키를 보내는 것을 수반하지 않습니다.)

인증이 요청되었지만 인증 키가 지정되지 않으면, current_process().authkey 의 반환 값이 사용됩니다 (Process 를 보세요). 이 값은 현재 프로세스가 생성하는 Process 객체에 의해 자동으로 상속됩니다. 이것은 다중 프로세스 프로그램의 모든 프로세스는 (기본적으로) 자신들 간의 연결을 설정할 때 사용할 수 있는 하나의 인증 키를 공유한다는 것을 뜻합니다.

적절한 인증 키는 os.urandom() 을 사용하여 생성할 수도 있습니다.

### 로깅

로깅에 대한 일부 지원이 제공됩니다. 그러나, logging 패키지는 프로세스 공유 록을 사용하지 않으므로 (처리기형에 따라) 다른 프로세스의 메시지가 뒤섞일 가능성이 있습니다.

multiprocessing.get_logger()
multiprocessing에서 사용되는 로거를 반환합니다. 필요하다면, 새로운 것이 만들어집니다.

로거가 처음 생성되면 수준 logging.NOTSET 을 가지며 기본 처리기가 없습니다. 이 로거로 보낸 메시지는 기본적으로 루트 로거에 전파되지 않습니다.

윈도우에서 자식 프로세스는 부모 프로세스의 로거의 수준만 상속받습니다 -- 그 밖의 다른 로거 사용자 지정은 상속되지 않습니다.

multiprocessing.log_to_stderr()
이 함수는 get_logger()를 호출하지만, get_logger에 의해 생성된 로거를 반환하는 것 외에, '[%(levelname)s/%(processName)s] %(message)s' 포맷을 사용하여 sys.stderr 에 출력을 전송하는 처리기를 추가합니다.

다음은 로깅이 켜져 있는 예제 세션입니다:

>>>
>>> import multiprocessing, logging
>>> logger = multiprocessing.log_to_stderr()
>>> logger.setLevel(logging.INFO)
>>> logger.warning('doomed')
[WARNING/MainProcess] doomed
>>> m = multiprocessing.Manager()
[INFO/SyncManager-...] child process calling self.run()
[INFO/SyncManager-...] created temp directory /.../pymp-...
[INFO/SyncManager-...] manager serving at '/.../listener-...'
>>> del m
[INFO/MainProcess] sending shutdown message to manager
[INFO/SyncManager-...] manager exiting with exitcode 0
로깅 수준의 전체 표는 logging 모듈을 참조하십시오.

### multiprocessing.dummy 모듈

multiprocessing.dummy 는 multiprocessing 의 API를 복제하지만 threading 모듈에 대한 래퍼일 뿐입니다.

## 프로그래밍 지침

multiprocessing를 사용할 때 준수해야 할 지침과 관용구가 있습니다.

### 모든 시작 방법

다음은 모든 시작 방법에 적용됩니다.

공유 상태를 피하세요

가능한 한 프로세스 간에 많은 양의 데이터가 이동하지 않도록 해야 합니다.

저수준 동기화 프리미티브를 사용하기보다, 프로세스 간 통신을 위해 큐나 파이프를 사용하는 것이 아마도 최선입니다.

피클 가능성

프락시 메서드에 대한 인자가 피클 가능한지 확인하십시오.

프락시의 스레드 안전성

록으로 보호하지 않는 한 둘 이상의 스레드에서 프락시 객체를 사용하지 마십시오.

(여러 프로세스가 같은 프락시를 사용하는 문제는 존재하지 않습니다.)

좀비 프로세스 조인하기

유닉스에서 프로세스가 끝났지만 조인되지 않으면 좀비가 됩니다. 너무 많이 생기지는 않아야 하는데, 새로운 프로세스가 시작될 때마다 (또는 active_children() 이 호출 되면) 아직 조인되지 않은 모든 완료된 프로세스를 조인하기 때문입니다. 또한, 완료된 프로세스의 Process.is_alive 를 호출하면 조인합니다. 그렇다고 하더라도 여러분이 시작시키는 모든 프로세스를 명시적으로 조인하는 것이 좋습니다.

피클/언 피클보다 상속하는 것이 더 좋습니다.

spawn 이나 forkserver 시작 방법을 사용할 때, multiprocessing 의 여러 형은 자식 프로세스가 사용할 수 있도록 피클 가능할 필요가 있습니다. 그러나, 일반적으로 파이프나 큐를 사용하여 공유 객체를 다른 프로세스로 보내는 것을 피해야 합니다. 대신 다른 곳에 만들어진 공유 자원에 접근해야 하는 프로세스가 조상 프로세스에서 그것들을 상속받을 수 있도록 프로그램을 배치해야 합니다.

프로세스 강제 종료를 피하세요

Process.terminate 메서드를 사용해서 프로세스를 정지시키는 것은, 그 프로세스가 현재 사용하고 있는 공유 자원(가령 록, 세마포어, 파이프, 큐)을 손상하거나 다른 프로세스에서 사용할 수 없게 만들 수 있습니다.

따라서, 아마도 어떤 공유 자원도 사용하지 않는 프로세스에만 Process.terminate 사용을 고려하는 것이 최선일 겁니다.

큐를 사용하는 프로세스 조인하기

큐에 항목을 넣은 프로세스는 종료되기 전에 버퍼링 된 모든 항목이 "피더" 스레드에 의해 하부 파이프로 공급될 때까지 대기합니다. (자식 프로세스는 Queue.cancel_join_thread 메서드를 호출해서 이 동작을 회피할 수 있습니다.)

이것은, 큐를 사용할 때마다 큐에 넣은 모든 항목이 결국 프로세스가 조인되기 전에 제거되도록 해야 함을 의미합니다. 그렇지 않으면 큐에 항목을 넣은 프로세스가 종료되리라고 보장할 수 없습니다. 데몬이 아닌 프로세스가 자동으로 조인된다는 것도 기억하세요.

교착 상태에 빠지는 예는 다음과 같습니다:

from multiprocessing import Process, Queue

def f(q):
    q.put('X' * 1000000)

if __name__ == '__main__':
    queue = Queue()
    p = Process(target=f, args=(queue,))
    p.start()
    p.join()                    # this deadlocks
    obj = queue.get()
이 문제를 고치는 방법은 마지막 두 줄의 순서를 바꾸는 것입니다 (또는 간단히 p.join() 줄을 지우는 것입니다).

자식 프로세스에 자원을 명시적으로 전달하세요.

fork 시작 방법을 사용하는 유닉스에서, 자식 프로세스는 전역 자원을 사용하여 부모 프로세스에서 생성된 공유 자원을 사용할 수 있습니다. 그러나 자식 프로세스의 생성자에 객체를 인자로 전달하는 것이 더 좋습니다.

윈도우 및 다른 시작 방법과 (잠재적으로) 호환될 수 있는 코드를 만드는 것 외에도, 이것은 자식 프로세스가 아직 살아있는 동안 객체가 부모 프로세스에서 가비지 수집되지 않음을 보장합니다. 부모 프로세스에서 그 객체가 가비지 수집될 때 일부 자원이 해제되면 이것이 중요 할 수 있습니다.

그래서 예를 들면

from multiprocessing import Process, Lock

def f():
    ... do something using "lock" ...

if __name__ == '__main__':
    lock = Lock()
    for i in range(10):
        Process(target=f).start()
는 다음과 같이 다시 써야 합니다

from multiprocessing import Process, Lock

def f(l):
    ... do something using "l" ...

if __name__ == '__main__':
    lock = Lock()
    for i in range(10):
        Process(target=f, args=(lock,)).start()
sys.stdin 을 "파일류 객체"로 교체할 때 조심하세요

multiprocessing은 원래 무조건 다음과 같이 호출했습니다

os.close(sys.stdin.fileno())
multiprocessing.Process._bootstrap() 메서드에서 하는 작업입니다 --- 이것은 손자 프로세스와 관련된 문제로 이어졌습니다. 이것은 다음과 같이 변경되었습니다:

sys.stdin.close()
sys.stdin = open(os.open(os.devnull, os.O_RDONLY), closefd=False)
이것은 프로세스가 서로 충돌해서 파일 기술자 에러를 일으키는 근본적인 문제를 해결하지만, sys.stdin() 을 출력 버퍼링을 사용하는 "파일과 유사한 객체"로 교체하는 응용 프로그램에 잠재적 위험을 만듭니다. 이 위험은, 다중 프로세스가 이 파일류 객체에 close()를 호출하면, 같은 데이터가 객체에 여러 번 플러시 되도록 만들어 손상을 일으킬 수 있다는 것입니다.

파일류 객체를 작성하고 여러분 자신의 캐싱을 구현하면, 캐시에 추가할 때마다 pid를 저장하고, pid가 변경되면 캐시를 버려서 포크에 안전하게 만들 수 있습니다. 예를 들면:

@property
def cache(self):
    pid = os.getpid()
    if pid != self._pid:
        self._pid = pid
        self._cache = []
    return self._cache
자세한 내용은 bpo-5155, bpo-5313 및 bpo-5331을 참조하십시오.

### spawn과 forkserver 시작 방법

fork 시작 방법에는 적용되지 않는 몇 가지 추가 제한 사항이 있습니다.

더 높은 피클 가능성

Process.__init__() 에 대한 모든 인자가 피클 가능한지 확인하십시오. 또한, Process 의 서브 클래스를 만들면, Process.start 메서드가 호출될 때 그 인스턴스가 피클 가능하도록 해야 합니다.

전역 변수

자식 프로세스에서 실행되는 코드가 전역 변수에 접근하려고 시도하면, 그 값은 (있는 경우) Process.start 가 호출되는 시점의 부모 프로세스의 값과 같지 않을 수 있습니다.

하지만, 모듈 수준의 상수인 전역 변수는 문제가 되지 않습니다.

메인 모듈의 안전한 임포트

메인 모듈이 의도하지 않은 부작용(가령 새 프로세스 시작)을 일으키지 않고 새 파이썬 인터프리터가 안전하게 임포트 할 수 있는지 확인하십시오.

예를 들어, spawn 또는 forkserver 시작 방법을 사용해서 다음 모듈을 실행하면 RuntimeError 로 실패합니다:

from multiprocessing import Process

def foo():
    print('hello')

p = Process(target=foo)
p.start()
대신 다음과 같이 if __name__ == '__main__': 을 사용하여 프로그램의 "진입 지점"을 보호해야 합니다:

from multiprocessing import Process, freeze_support, set_start_method

def foo():
    print('hello')

if __name__ == '__main__':
    freeze_support()
    set_start_method('spawn')
    p = Process(target=foo)
    p.start()
(freeze_support() 줄은 프로그램이 프로즌 되지 않고 정상적으로 실행될 경우 생략될 수 있습니다.)

이것은 새로 스폰 된 파이썬 인터프리터가 모듈을 안전하게 임포트 한 다음 모듈의 foo() 함수를 실행할 수 있게 해줍니다.

메인 모듈에서 풀이나 관리자를 만들면 비슷한 제한이 적용됩니다.

## 예제
사용자 정의된 관리자와 프락시를 만들고 사용하는 방법에 대한 시연:

from multiprocessing import freeze_support
from multiprocessing.managers import BaseManager, BaseProxy
import operator

##

class Foo:
    def f(self):
        print('you called Foo.f()')
    def g(self):
        print('you called Foo.g()')
    def _h(self):
        print('you called Foo._h()')

# A simple generator function
def baz():
    for i in range(10):
        yield i*i

# Proxy type for generator objects
class GeneratorProxy(BaseProxy):
    _exposed_ = ['__next__']
    def __iter__(self):
        return self
    def __next__(self):
        return self._callmethod('__next__')

# Function to return the operator module
def get_operator_module():
    return operator

##

class MyManager(BaseManager):
    pass

# register the Foo class; make `f()` and `g()` accessible via proxy
MyManager.register('Foo1', Foo)

# register the Foo class; make `g()` and `_h()` accessible via proxy
MyManager.register('Foo2', Foo, exposed=('g', '_h'))

# register the generator function baz; use `GeneratorProxy` to make proxies
MyManager.register('baz', baz, proxytype=GeneratorProxy)

# register get_operator_module(); make public functions accessible via proxy
MyManager.register('operator', get_operator_module)

##

def test():
    manager = MyManager()
    manager.start()

    print('-' * 20)

    f1 = manager.Foo1()
    f1.f()
    f1.g()
    assert not hasattr(f1, '_h')
    assert sorted(f1._exposed_) == sorted(['f', 'g'])

    print('-' * 20)

    f2 = manager.Foo2()
    f2.g()
    f2._h()
    assert not hasattr(f2, 'f')
    assert sorted(f2._exposed_) == sorted(['g', '_h'])

    print('-' * 20)

    it = manager.baz()
    for i in it:
        print('<%d>' % i, end=' ')
    print()

    print('-' * 20)

    op = manager.operator()
    print('op.add(23, 45) =', op.add(23, 45))
    print('op.pow(2, 94) =', op.pow(2, 94))
    print('op._exposed_ =', op._exposed_)

##

if __name__ == '__main__':
    freeze_support()
    test()
Pool 사용하기:

import multiprocessing
import time
import random
import sys

#
# Functions used by test code
#

def calculate(func, args):
    result = func(*args)
    return '%s says that %s%s = %s' % (
        multiprocessing.current_process().name,
        func.__name__, args, result
        )

def calculatestar(args):
    return calculate(*args)

def mul(a, b):
    time.sleep(0.5 * random.random())
    return a * b

def plus(a, b):
    time.sleep(0.5 * random.random())
    return a + b

def f(x):
    return 1.0 / (x - 5.0)

def pow3(x):
    return x ** 3

def noop(x):
    pass

#
# Test code
#

def test():
    PROCESSES = 4
    print('Creating pool with %d processes\n' % PROCESSES)

    with multiprocessing.Pool(PROCESSES) as pool:
        #
        # Tests
        #

        TASKS = [(mul, (i, 7)) for i in range(10)] + \
                [(plus, (i, 8)) for i in range(10)]

        results = [pool.apply_async(calculate, t) for t in TASKS]
        imap_it = pool.imap(calculatestar, TASKS)
        imap_unordered_it = pool.imap_unordered(calculatestar, TASKS)

        print('Ordered results using pool.apply_async():')
        for r in results:
            print('\t', r.get())
        print()

        print('Ordered results using pool.imap():')
        for x in imap_it:
            print('\t', x)
        print()

        print('Unordered results using pool.imap_unordered():')
        for x in imap_unordered_it:
            print('\t', x)
        print()

        print('Ordered results using pool.map() --- will block till complete:')
        for x in pool.map(calculatestar, TASKS):
            print('\t', x)
        print()

        #
        # Test error handling
        #

        print('Testing error handling:')

        try:
            print(pool.apply(f, (5,)))
        except ZeroDivisionError:
            print('\tGot ZeroDivisionError as expected from pool.apply()')
        else:
            raise AssertionError('expected ZeroDivisionError')

        try:
            print(pool.map(f, list(range(10))))
        except ZeroDivisionError:
            print('\tGot ZeroDivisionError as expected from pool.map()')
        else:
            raise AssertionError('expected ZeroDivisionError')

        try:
            print(list(pool.imap(f, list(range(10)))))
        except ZeroDivisionError:
            print('\tGot ZeroDivisionError as expected from list(pool.imap())')
        else:
            raise AssertionError('expected ZeroDivisionError')

        it = pool.imap(f, list(range(10)))
        for i in range(10):
            try:
                x = next(it)
            except ZeroDivisionError:
                if i == 5:
                    pass
            except StopIteration:
                break
            else:
                if i == 5:
                    raise AssertionError('expected ZeroDivisionError')

        assert i == 9
        print('\tGot ZeroDivisionError as expected from IMapIterator.next()')
        print()

        #
        # Testing timeouts
        #

        print('Testing ApplyResult.get() with timeout:', end=' ')
        res = pool.apply_async(calculate, TASKS[0])
        while 1:
            sys.stdout.flush()
            try:
                sys.stdout.write('\n\t%s' % res.get(0.02))
                break
            except multiprocessing.TimeoutError:
                sys.stdout.write('.')
        print()
        print()

        print('Testing IMapIterator.next() with timeout:', end=' ')
        it = pool.imap(calculatestar, TASKS)
        while 1:
            sys.stdout.flush()
            try:
                sys.stdout.write('\n\t%s' % it.next(0.02))
            except StopIteration:
                break
            except multiprocessing.TimeoutError:
                sys.stdout.write('.')
        print()
        print()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    test()
큐를 사용하여 작업을 작업자 프로세스 집단에 제공하고 결과를 수집하는 방법을 보여주는 예:

import time
import random

from multiprocessing import Process, Queue, current_process, freeze_support

#
# Function run by worker processes
#

def worker(input, output):
    for func, args in iter(input.get, 'STOP'):
        result = calculate(func, args)
        output.put(result)

#
# Function used to calculate result
#

def calculate(func, args):
    result = func(*args)
    return '%s says that %s%s = %s' % \
        (current_process().name, func.__name__, args, result)

#
# Functions referenced by tasks
#

def mul(a, b):
    time.sleep(0.5*random.random())
    return a * b

def plus(a, b):
    time.sleep(0.5*random.random())
    return a + b

#
#
#

def test():
    NUMBER_OF_PROCESSES = 4
    TASKS1 = [(mul, (i, 7)) for i in range(20)]
    TASKS2 = [(plus, (i, 8)) for i in range(10)]

    # Create queues
    task_queue = Queue()
    done_queue = Queue()

    # Submit tasks
    for task in TASKS1:
        task_queue.put(task)

    # Start worker processes
    for i in range(NUMBER_OF_PROCESSES):
        Process(target=worker, args=(task_queue, done_queue)).start()

    # Get and print results
    print('Unordered results:')
    for i in range(len(TASKS1)):
        print('\t', done_queue.get())

    # Add more tasks using `put()`
    for task in TASKS2:
        task_queue.put(task)

    # Get and print some more results
    for i in range(len(TASKS2)):
        print('\t', done_queue.get())

    # Tell child processes to stop
    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')


if __name__ == '__main__':
    freeze_support()
    test()