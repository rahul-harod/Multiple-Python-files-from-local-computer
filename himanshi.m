
global D sigma sigma0 mu0;
mu0=[12 28];
sigma0=[9 0;0 8];
sigma=[16 0; 0 9];
D =[10.3 34.2;12.2 31.1;8.5 35.7;14.2 30.8];
a1=0;
a2=30;
b1=20;
b2=40;
delta1=0.2;
delta2=0.2;
theta1=a1:delta1:a2;
theta2=b1:delta2:b2;
q=zeros(length(theta1),length(theta2));




for i=1:length(theta1)
    for j=1:length(theta2)
        q(i,j)=qfun(theta1(i),theta2(j));
    end
end

function s=qfun(param1,param2)
    global D mu0 sigma0 sigma;
    x=[param1, param2];
    mu=x;
    like=mvnpdf(D,mu,sigma);
    prior=mvnpdf(mu,mu0,sigma0);
    s=prod(like)*prior;

end 



        