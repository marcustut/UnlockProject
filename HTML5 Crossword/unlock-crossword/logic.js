function startGame() {
    class CrosswordRow {
        constructor(answer, typedAnswer) {
            this.answer = answer;
            this.typedAnswer = typedAnswer;
        }
    }

    var row0 = new CrosswordRow("I", "");
    var row1 = new CrosswordRow("SD", "");
    var row2 = new CrosswordRow("QUIXOTICY", "");
    var row3 = new CrosswordRow("HL", "");
    var row4 = new CrosswordRow("GLOCKENSPIEL", "");
    var row5 = new CrosswordRow("ZI", "");
    var row6 = new CrosswordRow("EOC", "");
    var row7 = new CrosswordRow("MISSISSIPPIS", "");
    var row8 = new CrosswordRow("DHG", "");
    var row9 = new CrosswordRow("OZRR", "");
    var row10 = new CrosswordRow("SPARAPHERNALIA", "");
    var row11 = new CrosswordRow("FNF", "");
    var row12 = new CrosswordRow("TIF", "");
    var row13 = new CrosswordRow("ILARYNXI", "");
    var row14 = new CrosswordRow("GT", "");
    var row15 = new CrosswordRow("O", "");

    var Crossword = [row0, row1, row2, row3, row4, row5, row6, row7, row8, row9, row10, row11, row12, row13, row14, row15];


    var numberChecker = 0;


    function skipToNext(elem) {
        var nextElemIndex = parseFloat(elem.getAttribute('tabindex')) + 1;
        document.querySelector('[tabindex="' + nextElemIndex + '"]').focus();
    }


    document.getElementById("submit_crossword").addEventListener("click", function (e) {
        // Prevent webpage from refreshing
        e.preventDefault();


        numberChecker = 0;
        // Loop through each rows
        for (var j = 0; j < Crossword.length; j++) {
            Crossword[j].typedAnswer = "";

            // Loop through each columns
            for (var i = 0; i < Crossword[j].answer.length; i++) {
                // Adding value of each columns to Crossword.typedAnswer
                Crossword[j].typedAnswer += document.getElementById("cross-row" + j.toString()).querySelectorAll("input")[i].value.toUpperCase();
            }


            // Check if typedAnswer is equal to Answer
            if (Crossword[j].typedAnswer === Crossword[j].answer) {
                // If equal, good answer(remove bad, add good)
                document.getElementById("cross-row" + j.toString()).classList.remove("bad");
                document.getElementById("cross-row" + j.toString()).classList.add("good");
                // Increment numberChecker
                numberChecker++;
            } else {
                // If not equal, bad answer(remove good, add bad)
                document.getElementById("cross-row" + j.toString()).classList.remove("good");
                document.getElementById("cross-row" + j.toString()).classList.add("bad");
            }
        }

        if (numberChecker == Crossword.length) {
            var highlightedWord = document.querySelectorAll('input[data-type="hightlight"]')
            for (var k = 0; k < highlightedWord.length; k++) {
                highlightedWord[k].classList.add("main-highlighted");
            }

        }
    });
}

//adapted from https://codepen.io/arisusaktos
