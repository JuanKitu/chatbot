  ALEXIA: Spanish AIML brain
-------------------------------
  versión 1.5 2008/02/14
-------------------------------
     GALAIA Project
http://papa.det.uvigo.es/galaia


*** This brain version is optimized to use with Program E ***


IMPORTANT NOTE:
----------------

Sabela and Alexia's brains, after some questions to know the user, are designed to talk about the Galaia Project. This is achieved through a recursion the galaia.aiml file, where the info of the project is stored. This recursion is made through the infoUsuario.aiml file. If you want to customize the brains for other proyect, entreprise, etc. just perfom this two changes:

 > In the infoUsuario.aiml file, inside the askspecifictopic category, substitute the <srai>galaiatopic</srai> recursion for another to the desired topic.

 > Substitute the galaia.aiml file for another more suited to your needs.

It is neccesary to say, that for a brain to work coherently, some substitutions and splitters have to be defined. We have defined the following ones:


<!--Substitutions are grouped according to several AIML interpreter functions.-->
<substitutions lang="es">
  <input>
    <substitute find="Á" replace="A"/>
    <substitute find="É" replace="E"/>
    <substitute find="Í" replace="I"/>
    <substitute find="Ó" replace="O"/>
    <substitute find="Ú" replace="U"/>
    <substitute find="¿" replace=" "/>
    <substitute find="!" replace=" "/>
    <substitute find=":" replace=" "/>
    <substitute find="," replace=" "/>
  </input>
  <gender>
    <substitute find="la" replace="el"/>
  </gender>
  <person>
    <substitute find=" Yo " replace=" El "/>
  </person>
  <person2>
    <substitute find="yo" replace="tu"/>
    <substitute find="tu" replace="yo"/>
    <substitute find="eres" replace="soy"/>
    <substitute find="soy" replace="eres"/>
    <substitute find="estas" replace="estoy"/> <!-- Ojo!! Sin tilde -->
    <substitute find="estoy" replace="estas"/>
    <substitute find="irme" replace="irte"/>
    <substitute find="irte" replace="irme"/>
  </person2>
</substitutions>


<substitutions lang="gz">
  <input>
    <substitute find="Á" replace="A"/>
    <substitute find="É" replace="E"/>
    <substitute find="Í" replace="I"/>
    <substitute find="Ó" replace="O"/>
    <substitute find="Ú" replace="U"/>
    <substitute find="¿" replace=" "/>
    <substitute find="!" replace=" "/>
    <substitute find=":" replace=" "/>
    <substitute find="," replace=" "/>
  </input>
  <gender>
    <substitute find="a" replace="o"/>
  </gender>
  <person>
    <substitute find="eu" replace="el"/>
  </person>
  <person2>
    <substitute find="eu" replace="ti"/>
    <substitute find="ti" replace="eu"/>
    <substitute find="es" replace="son"/>
    <substitute find="son" replace="es"/>
    <substitute find="estas" replace="estou"/> <!-- Ojo!! Sin tilde -->
    <substitute find="estou" replace="estas"/>
    <substitute find="irme" replace="irte"/>
    <substitute find="irte" replace="irme"/>
  </person2>
</substitutions>

<substitutions lang="en">
  <input>
    <substitute find=":" replace=" "/>
    <substitute find="," replace=" "/>
  </input>
  <gender>
    <substitute find="he" replace="she"/>
    <substitute find="she" replace="he"/>
    <substitute find="his" replace="her"/>
  </gender>
  <person>
    <substitute find="I" replace="he"/>
  </person>
  <person2>
    <substitute find="I" replace="you"/>
    <substitute find="you" replace="I"/>
    <substitute find="is" replace="am"/>
    <substitute find="am" replace="is"/>
  </person2>
</substitutions>

<!--Sentence splitters defined strings that mark the end of a sentence,
             after input substitutions have been performed.-->
<sentence-splitters>
  <splitter value=";"/>
  <splitter value="."/>
  <splitter value="!"/>
  <splitter value="?"/>
</sentence-splitters>
