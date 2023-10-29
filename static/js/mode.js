
// get detfault mode
var mode = localStorage.getItem('interview_ready_mode');
console.log(mode)
// check if mode is dark
if (mode == 'dark' || mode == null){
    changeCss('dark');
}
else{
    changeCss('light');
}


function changeCss(mode){
    if (mode == 'dark'){
        // change css to dark mode
        document.getElementById('dark_css').disabled = false;
        document.getElementById('light_css').disabled = true;
        document.getElementById('toastcss').disabled = true;
        document.getElementById('moon').style.display = 'none';
        document.getElementById('sun').style.display = 'block';
        // set this as default
        localStorage.setItem('interview_ready_mode', 'dark');

        // for interview result

        // For overall score 
        let test = document.getElementById('overallscore_inner')
        if (test != null){
            var per = document.getElementById('overallscore_inner').getAttribute('data-before')
            var gradientValue = `radial-gradient(closest-side, #1f1e1e 79%, transparent 80% 100%), conic-gradient(#ffcf5e ${per}, #ffefc8 0)`;
            document.getElementById('overallscore_inner').style.background = gradientValue;

            // For grammar score
            var per = document.getElementById('grammar_score_inner').getAttribute('data-before')
            var gradientValue = `radial-gradient(closest-side, #1f1e1e 79%, transparent 80% 100%), conic-gradient(#57CDFD ${per}, #d5f4ff 0)`;
            document.getElementById('grammar_score_inner').style.background = gradientValue;

            // For clarity score
            var per = document.getElementById('clarity_score_inner').getAttribute('data-before')
            var gradientValue = `radial-gradient(closest-side, #1f1e1e 79%, transparent 80% 100%), conic-gradient(#9CA7EB ${per}, #d8ddff 0)`;
            document.getElementById('clarity_score_inner').style.background = gradientValue;


            // For confidence score
            let test2 = document.getElementById('confidence_score_inner')
            if (test2!=null){
                var per = document.getElementById('confidence_score_inner').getAttribute('data-before') 
                var gradientValue = `radial-gradient(closest-side, #1f1e1e 79%, transparent 80% 100%), conic-gradient(#d19ceb ${per}, rgb(221, 225, 255) 0)`;
                document.getElementById('confidence_score_inner').style.background = gradientValue;
            }

            // For interviewer score
            var per = document.getElementById('interviewer_score_inner').getAttribute('data-before')
            var gradientValue = `radial-gradient(closest-side, #1f1e1e 79%, transparent 80% 100%), conic-gradient(#FC8ECB ${per}, #ffd4ec 0)`;
            document.getElementById('interviewer_score_inner').style.background = gradientValue;
        }

    }
    else{
        // change css to light mode
        document.getElementById('dark_css').disabled = true;
        document.getElementById('light_css').disabled = false;
        document.getElementById('toastcss').disabled = false;
        document.getElementById('moon').style.display = 'block';
        document.getElementById('sun').style.display = 'none';
        // set this as default
        localStorage.setItem('interview_ready_mode', 'light');

        // for interview result

        // For overall score 
        let test = document.getElementById('overallscore_inner')
        if (test != null){
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
            let test2 = document.getElementById('confidence_score_inner')
            if (test2!=null){
                var per = document.getElementById('confidence_score_inner').getAttribute('data-before')
                var gradientValue = `radial-gradient(closest-side, white 79%, transparent 80% 100%), conic-gradient(#d19ceb ${per}, rgb(221, 225, 255) 0)`;
                document.getElementById('confidence_score_inner').style.background = gradientValue;
            }

            // For interviewer score
            var per = document.getElementById('interviewer_score_inner').getAttribute('data-before')
            var gradientValue = `radial-gradient(closest-side, white 79%, transparent 80% 100%), conic-gradient(#FC8ECB ${per}, #ffd4ec 0)`;
            document.getElementById('interviewer_score_inner').style.background = gradientValue;
        }


    }
}