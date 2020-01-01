import React, { Component } from "react";
import "../stylesheets/Question.css";

class Question extends Component {
  constructor() {
    super();
    this.state = {
      visibleAnswer: false
    };
  }

  flipVisibility() {
    this.setState({ visibleAnswer: !this.state.visibleAnswer });
  }

  render() {
    const { question, answer, category, difficulty } = this.props;
    console.log("Q: ", category);
    return (
      <div className="Question-holder">
        <div className="Question">{question}</div>
        <div className="Question-status">
          {category && (
            <img className="category" src={`${category.type}.svg`} alt={category.name} />
          )}
          <div className="difficulty">Difficulty: {difficulty}</div>
          <img
            alt="Delete category"
            src="delete.png"
            className="delete"
            onClick={() => this.props.questionAction("DELETE")}
          />
        </div>
        <div className="show-answer button" onClick={() => this.flipVisibility()}>
          {this.state.visibleAnswer ? "Hide" : "Show"} Answer
        </div>
        <div className="answer-holder">
          <span style={{ visibility: this.state.visibleAnswer ? "visible" : "hidden" }}>
            Answer: {answer}
          </span>
        </div>
      </div>
    );
  }
}

export default Question;