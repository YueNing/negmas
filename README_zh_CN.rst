.. image:: https://img.shields.io/pypi/pyversions/negmas.svg
    :target: https://pypi.python.org/pypi/negmas
    :alt: Python

.. image:: https://img.shields.io/pypi/status/negmas.svg
    :target: https://pypi.python.org/pypi/negmas
    :alt: Pypi

.. image:: https://img.shields.io/pypi/l/negmas.svg
    :target: https://pypi.python.org/pypi/negmas
    :alt: License

.. image:: https://img.shields.io/pypi/dm/negmas.svg
    :target: https://pypi.python.org/pypi/negmas
    :alt: Downloads

.. image:: https://img.shields.io/codacy/coverage/1b204fe0a69e41a298a175ea225d7b81.svg
    :target: https://app.codacy.com/project/yasserfarouk/negmas/dashboard
    :alt: Coveage

.. image:: https://img.shields.io/codacy/grade/1b204fe0a69e41a298a175ea225d7b81.svg
    :target: https://app.codacy.com/project/yasserfarouk/negmas/dashboard
    :alt: Code Quality

.. image:: https://img.shields.io/pypi/v/negmas.svg
    :target: https://pypi.python.org/pypi/negmas
    :alt: Pypi

.. image:: https://img.shields.io/travis/yasserfarouk/negmas.svg
    :target: https://travis-ci.org/yasserfarouk/negmas
    :alt: Build Status

.. image:: https://readthedocs.org/projects/negmas/badge/?version=latest
    :target: https://negmas/readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black
    :alt: Coding style black

NegMAS 是一个Python仿真库，用以模拟开发自动谈判代理。negmas意为谈判多代理系统（NEGotiation MultiAgent System）或者代理仿真的谈判管理（NEGotiations Managed by Agent Simulations）.
NegMAS的主要目标是推进现场同步谈判的研究和技术发展。当然可以并已被用于模拟更简单的双边、多边谈判、偏好启发等领域。

.. note:: 教程视频（ANAC2019_ 国际自动谈判代理人竞赛， SCM_）：YouTube地址_

    .. _ANAC2019: http://web.tuat.ac.jp/~katfuji/ANAC2019
    .. _SCM: http://web.tuat.ac.jp/~katfuji/ANAC2019/#scm
    .. _YouTube地址: https://www.youtube.com/playlist?list=PLqvs51K2Mb8LlUQk2DHLGnWdGqhXMNOM-

介绍
============

该库设计致力于在自动谈判中现场同步谈判（同步协商）领域上，通过提供易于使用并功能强大的平台，提高谈判领域研究和技术发展。产生于NEC和AIST的实验室合作项目。

*现场* 谈判意为效用函数非预先明令定义，而是通过模拟类商业过程产生的结果的一类模拟过程的集合。

*同步* 谈判意为某会谈协议的效用值受其他会谈发生的情况的影响。

详细文档地址: 文档_

.. _documentation: https://negmas.readthedocs.io/
.. _文档: https://negmas.readthedocs.io/

主要特点
=============

该仿真平台在设计初期就考虑并兼顾了灵活性和可扩展性。NegMAS的主要特点如下：

#. 公共API与内部细节脱钩，从而允许相同交互协议的可伸缩实现。

#. 支持代理商进行多个并发谈判。

#. 通过耦合效用函数或中央 *控制* 代理提供谈判间同步支持。
#. 提供示例谈判者，可以作为复杂谈判者的模板。
#. 同时支持调解和非调解（有无中间人介入）谈判。
#. 同时支持双边和多变谈判。
#. 同添加新谈判者一样，添加谈判协议和模拟世界也同样容易。
#. 允许像动态进出谈判等非传统谈判场景。
#. 大量的内置效用函数。
#. 效用函数可以是活跃的动态实体，对比存在的包，允许系统建模范围更广的效用函数（ufuns）。
#. 正在实现拥有相同接口的分布式系统并达到工业级别实现，从而允许NegMAS中开发的代理也可被部署在现实世界的商业行为中。

项目中使用negmas

.. code-block:: python

    import negmas

可在多场景中使用。一个特殊场景，端对端用户，尝试内建的谈判协议。另一个特殊场景，可用于开发多种不同的优秀谈判代理，谈判协议，多代理仿真（通常涉及到现场谈判）等等。

运行内置的谈判者，谈判协议
==================================================

如下代码所示，实现谈判

.. code-block:: python

    from negmas import SAOMechanism, AspirationNegotiator, MappingUtilityFunction
    session = SAOMechanism(outcomes=10, n_steps=100)
    negotiators = [AspirationNegotiator(name=f'a{_}') for _ in range(5)]
    for negotiator in negotiators:
        session.add(negotiator, ufun=MappingUtilityFunction(lambda x: random.random() * x[0]))

    session.run()

代码中，首先创建了一个带有十个离散输出，可运行100步的会谈机制。然后创建了五个带有随机效用函数的代理。然后运行会谈直到结束。通过会谈的 *state* 成员访问协议（如果有）。
库中提供了多种分析和可以化工具可用以查看谈判。有关更多详细信息，请参见第一个教程关于 *Running a Negotiation* 的章节。


谈判者开发
=======================

添加几行代码开发出新型谈判者

.. code-block:: python

    from negmas.sao import SAONegotiator
    from negmas import ResponseType
    class MyAwsomeNegotiator(SAONegotiator):
        def __init__(self):
            # initialize the parents
            super().__init__(self)

        def respond(self, offer, state):
            # decide what to do when receiving an offer
            return ResponseType.ACCEPT_OFFER

        def propose(self, state):
            # proposed the required number of proposals (or less) 
            pass

实现 `respond()` 和 `propose()` 两个函数。该谈判者现在可以参与交替报价谈判。有关可用功能的完整描述，请参阅文档 `Negotiator` 章节。


谈判协议开发
=================================

Developing a novel negotiation protocol is actually even simpler:

.. code-block:: python

    from negmas.mechanisms import Mechanism

    class MyNovelProtocol(Mechanism):
        def __init__(self):
            super().__init__()

        def round(self):
            # one step of the protocol
            pass

通过实现单个 `round()` 函数创建一个新的协议。 新的谈判者可以通过调用 `add()` 和 `remove()` 加入离开谈判。
请参阅文档以获取有关“机制”可用功能的完整说明（另外，可以使用“协议”代替“机制”）。

运行模拟世界
==========================

NegMAS的 *理由* 是允许您开发能够在现实的 *类似商业* 模拟环境中运行的谈判代理。 这些模拟在NegMAS中称为“世界”。 
代理在这些模拟环境中相互交互，试图通过几次（可能同时）协商来最大化代理的某些内在效用函数。

`situated` 模块提供了创建此类世界所需的全部。 例子可以在 `scml` 包中找到。
该包实现模拟了一个供应链管理系统，在该系统中，工厂经理仅通过谈判作为获得合同的手段，就可以在市场竞争中最大化自己的利润。


致谢
===============

.. _Genius: http://ii.tudelft.nl/genius

NegMAS测试，使用从 Genius_ 平台获得的ANAC 2010到ANAC 2018竞赛中使用的场景。这些可以在测试/数据和笔记本/数据文件夹中找到。

