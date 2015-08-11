
편의를 위해 간결체 혹은 음슴체로(...) 작성합니다



#Triton 스크립트 기본 작성법


[callback_after.py](https://github.com/laughfool/Triton/blob/master/examples/callback_after.py) 을 참조하도록 함. 위 코드에서 스크립트의 기본적인 틀을 볼 수 있다. 

###메인함수
main 스크립트 작성 과정은 대충 아래와 같다.


1. 분석할 함수 선택
2. 콜백함수 등록
3. 프로그램 실행


**startAnalysisFromSymbol(<함수명>)** 을 통해 분석하고자 하는 함수를 선택 가능하다. 만약 main 함수를 분석하려고 하면 main 이라고 주면 된다.
strip 되어 있거나 함수의 이름을 모르는 경우에는 주소값으로도 지정해 줄 수 있다.
**triton.startAnalysysFromAddr(<주소>) / triton.stopAnalysysFromAddr(<주소>)**

###콜백함수
메인에서는 3가지 유형의 콜백 함수를 등록할 수 있다(BEFORE, AFTER, FIN). 주로 BEFORE / AFTER 를 많이 사용하며 FIN 은 추후 추가 설명.

기본적으로 콜백 함수의 argument 는 instruction 이 들어가는데, 이 instruction 객체를 통해 어셈코드를 얻거나, 레지스터 값을 얻거나, 각종 원하는 짓거리를 다 할 수 있다. instruction 객체를 자유자재로 쓰는 것이 매우 중요하다. instruction 은 따로 설명이 필요할 것이다.

3가지 콜백은 이름 그대로.. BEFORE 는 instruction 실행 전에, AFTER 는 instruction 실행 후이며, FIN 은 **startAnalysisFromSymbol** 혹은 **startAnalysysFromAddress** 로 지정한 모든 분석이 끝난 후에 실행된다.

instruction 객체가 제공하는 **GetRegValue()** 또는 **getRegs()** 를 BEFORE 콜백과 AFTER 콜백에 동일하게 넣고 실행해보면 레지스터 값의 변화를 모니터링 할 수 있다.





