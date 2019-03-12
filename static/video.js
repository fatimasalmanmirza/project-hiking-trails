

$( document ).ready(function() {

    scaleAnimationContainer();

    initBannerAnimationSize('.animation-container .animation img');
    initBannerAnimationSize('.animation-container .mask');
    initBannerAnimationSize('.animation-container video');

    $(window).on('resize', function() {
        scaleAnimationContainer();
        scaleBannerAnimationSize('.animation-container .animation img');
        scaleBannerAnimationSize('.animation-container .mask');
        scaleBannerAnimationSize('.animation-container video');
    });

});

function scaleAnimationContainer() {

    var height = $(window).height() + 5;
    var unitHeight = parseInt(height) + 'px';
    $('.homepage-banner').css('height',unitHeight);

}

function initBannerAnimationSize(element){

    $(element).each(function(){
        $(this).data('height', $(this).height());
        $(this).data('width', $(this).width());
    });

    scaleBannerAnimationSize(element);

}

function scaleBannerAnimationSize(element){

    var windowWidth = $(window).width(),
    windowHeight = $(window).height() + 5,
    animationWidth,
    animationHeight;

    console.log(windowHeight);

    $(element).each(function(){
        var animationAspectRatio = $(this).data('height')/$(this).data('width');

        $(this).width(windowWidth);

        if(windowWidth < 1000){
            animationHeight = windowHeight;
            animationWidth = animationHeight / animationAspectRatio;
            $(this).css({'margin-top' : 0, 'margin-left' : -(animationWidth - windowWidth) / 2 + 'px'});

            $(this).width(animationWidth).height(animationHeight);
        }

        $('.homepage-banner .animation-container video').addClass('fadeIn animated');

    });
}