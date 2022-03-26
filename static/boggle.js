"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  let response = await axios.post("/api/new-game");
  gameId = response.data.gameId;
  let board = response.data.board;

  displayBoard(board);
}


/** Display board */

function displayBoard(board) {
  $table.empty();
  // loop over board and create the DOM tr/td structure
  for (let i = 0; i < board.length; i++){
    let $currentRow = $("<tr></tr>");

    for (let j = 0; j < board[i].length; j++){
      let letter = board[i][j]
      let $currentCell = $(`<td>${letter}</td>`);
      $currentRow.append($currentCell);
    }

    $table.append($currentRow);
  }
}

/**  */
async function handleSubmit(evt){
  evt.preventDefault();
  
  let response = await axios.post("/api/score-word", {"gameId": gameId, "word": $wordInput.val()});
  
  if (response.data.result === "not-on-board"){
    displayMessage("This word is not on the board");
  }
  else if(response.data.result === "not-word"){
    displayMessage("This is not a real word");
  }
  else{
    $playedWords.append(`<li>${$wordInput.val()}</li>`);
  }
}

function displayMessage(msg){
  $message.html(msg);
  setTimeout(function(){
    $message.html("");
  }, 2000)
}

$form.on("submit", handleSubmit);

start();