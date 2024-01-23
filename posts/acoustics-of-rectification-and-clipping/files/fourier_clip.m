sampl = 5000;
freq = 100;

p = panel();
p.pack(4,2);


t = 0:1/sampl:0.5-1/sampl;

fSin = sin(2*pi*freq*t);
fSinFFT = fft(fSin);
fHR = halfRecSin(t,freq);
fHRFFT = fft(fHR);     
fClip = clipSin(t,freq,0.5);
fClipFFT = fft(fClip);     
fAsymClip = asymClipSin(t,freq,0.5,-0.2);
fAsymClipFFT = fft(fAsymClip);

w = (0:length(fAsymClipFFT)-1)*sampl/length(fAsymClipFFT);

% plotting
p(1,1).select();
plot(t,fSin, 'LineWidth',2)
xlim([0, 0.1])
title('normal sine')

p(1,2).select();
plot(w, abs(fSinFFT), 'LineWidth',2)
xlim([5, 750])
title('normal sine FFT')


p(2,1).select();
plot(t,fHR, 'LineWidth',2)
xlim([0, 0.1])
title('half-rect sine')

p(2,2).select();
plot(w,abs(fHRFFT), 'LineWidth',2)
xlim([5, 750])
title('half-rect fft')


p(3,1).select();
plot(t,fClip, 'LineWidth',2)
title('clipped sine')
xlim([0, 0.1])

p(3,2).select();
plot(w,abs(fClipFFT), 'LineWidth',2)
xlim([5, 750])
title('clipped fft')

p(4,1).select();
plot(t,fAsymClip, 'LineWidth',2)
title('asymClipped sine')
xlim([0, 0.1])

p(4,2).select();
plot(w,abs(fAsymClipFFT), 'LineWidth',2)
xlim([5, 750])
title('asymClipped fft')

p.export('t11.png', '-w400', '-h200');
% funcs
function y = halfRecSin(t,freq)
    output = zeros(length(t));
    for i = 1:length(t)-1
        fnc = sin(2*pi*freq*t(i));
        if(fnc >= 0)
            output(i) = fnc;
        else
            output(i) = 0;
        end
    end
    y = output;
end
function y = clipSin(t,freq,clip)
    output = zeros(length(t));
    for i = 1:length(t)-1
        fnc = sin(2*pi*freq*t(i));
        if(fnc >= clip)
            output(i) = clip;
        elseif(fnc <= -clip)
            output(i) = -clip;
        else
            output(i) = fnc;
        end
    end
    y = output;
end
function y = asymClipSin(t,freq,clipPlus,clipMinus)
    output = zeros(length(t));
    for i = 1:length(t)-1
        fnc = sin(2*pi*freq*t(i));
        if(fnc >= clipPlus)
            output(i) = clipPlus;
        elseif(fnc <= clipMinus)
            output(i) = clipMinus;
        else
            output(i) = fnc;
        end
    end
    y = output;
end
