---
tocdepth: 4
---

```{admonition} TL;DR
:class: tip
See on this page: [Design Lab 03 (All Carrot, No Stick)](designLab3)
```

# Unit 2: Signals and Systems

## Lecture 3 Signals and Systems

### Lecture Handout

[Lecture 3 handout](https://ocw.mit.edu/courses/6-01sc-introduction-to-electrical-engineering-and-computer-science-i-spring-2011/921906c5cea95b6a532dbd727b62e33a_MIT6_01SCS11_lec03_handout.pdf)

### Readings

Read section 4.2 of the course notes.

- [Chapter 4: State Machines (PDF)](https://ocw.mit.edu/courses/6-01sc-introduction-to-electrical-engineering-and-computer-science-i-spring-2011/resources/mit6_01scs11_chap04/)

### My Notes

- Difference Equations- is Declarative
    - tells the true statement about what the system will do.
- Block Diagram - is Imperative
    - tells what to do now
- Abstraction is to use Signals instead of Samples
- Using Operators
    - Operator works on Signal only
    - Operator obeys commutivity
    - Operator multiplication is distributive in addition
    - Operator obeys distributivity

(designLab3)=
### Design Lab 03 (All Carrot, No Stick)

#### Objective: **Hip to be Square**

##### a. CombinedDynamicMoveToPoint

Propotional controller that performs both rotation and forward movement simultaneously towards the final point.
The Robot moves forward and rotates at the same time making it *combined* smooth motion.

:::{image} ./media/CombinedDynamicMoveToPoint(Both).gif
:alt: CombinedDynamicMoveToPoint
:::

##### b. SequentialDynamicMoveToPoint

Propotional controller that first performs rotation towards the direction of the final point and then moves towards it.
The Robot first rotates towards the goal, then moves forward making it a *sequential* motion.

```{eval-rst}
.. image:: ./media/SequentialDynamicMoveToPoint(Both).gif
    :alt: SequentialDynamicMoveToPoint
```


#### Objective 5. **I am a ballerina**

The robot gracefully dance the pattern of a secret message

![slimeTrail](./media/secretMessage.png)


````{dropdown} Source Code
:open:
```{eval-rst}
.. automodule:: dynamicMoveToPoint
   :members:
   :undoc-members:
```
````