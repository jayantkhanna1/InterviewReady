
// For overall score
var per = document.getElementById('overallscore_inner').getAttribute('data-before')
var gradientValue = `radial-gradient(closest-side, white 79%, transparent 80% 100%), conic-gradient(#ffcf5e ${per}, #ffefc8 0)`;
document.getElementById('overallscore_inner').style.background = gradientValue;

// For grammar score
var per = document.getElementById('grammar_score_inner').getAttribute('data-before')
var gradientValue = `radial-gradient(closest-side, white 79%, transparent 80% 100%), conic-gradient(#57CDFD ${per}, #d5f4ff 0)`;
document.getElementById('grammar_score_inner').style.background = gradientValue;

// For clarity score
var per = document.getElementById('clarity_score_inner').getAttribute('data-before')
var gradientValue = `radial-gradient(closest-side, white 79%, transparent 80% 100%), conic-gradient(#9CA7EB ${per}, #d8ddff 0)`;
document.getElementById('clarity_score_inner').style.background = gradientValue;


// For confidence score
// var per = document.getElementById('confidence_score_inner').getAttribute('data-before')
// var gradientValue = `radial-gradient(closest-side, white 79%, transparent 80% 100%), conic-gradient(#d19ceb ${per}, rgb(221, 225, 255) 0)`;
// document.getElementById('confidence_score_inner').style.background = gradientValue;

// For interviewer score
var per = document.getElementById('interviewer_score_inner').getAttribute('data-before')
var gradientValue = `radial-gradient(closest-side, white 79%, transparent 80% 100%), conic-gradient(#FC8ECB ${per}, #ffd4ec 0)`;
document.getElementById('interviewer_score_inner').style.background = gradientValue;
