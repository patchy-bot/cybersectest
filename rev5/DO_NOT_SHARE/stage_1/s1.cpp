#include <iostream>
#include <string>
#include "sha512.hpp"
using namespace std;
using namespace sw;

float _fun(float number) {
	long i;
	float x2, y;
	const float threehalfs = 1.5F;

	x2 = number * 0.5F;
	y = number;
	i = *(long *)&y;                       // evil floating point bit level hacking
	i = 0x5f3759df - (i >> 1);               // wtf?
	y = *(float *)&i;
	y = y * (threehalfs - (x2 * y * y));   // 1st iteration
	//	y  = y * ( threehalfs - ( x2 * y * y ) );   // 2nd iteration, this can be removed

	return y;
}

bool _fun1(const size_t& n) {
    bool flag1 = true;
    for (size_t i = 2; i <= (size_t)(1/_fun(n)); ++i)
        if (!(n%i))
            flag1 = false;
    return flag1;
}

bool _fun2(size_t n) {
    size_t root = (size_t)(1/_fun(n));
    return (root * root == n);
}

/////////////////////////////////////////////////////////////////////////////////////////////////

const inline bool function_1(const size_t& n) {
    if (n<0) return false;
    size_t x = 0;
    for (size_t i=1; x<=n; i++) {
        x += i;
        if (x==n) return true;
    } return false;
}

/////////////////////////////////////////////////////////////////////////////////////////////////

const inline bool function_2(const size_t& n) {
    if (!n) return true;
    size_t a = 0, b = 1, c = 1;
    while (c < n) a = b, b = c, c = a + b;
    return ((c == n | _fun2(5*n*n+4) | _fun2(5*n*n-4)) & _fun1(n));
}

/////////////////////////////////////////////////////////////////////////////////////////////////

const inline bool function_3(const size_t& n) {
    string _ = to_string(n);
    return _fun1(n)&(_==string(_.rbegin(), _.rend()));
}

/////////////////////////////////////////////////////////////////////////////////////////////////

const string cmp_sha_a = "a0c4746b5db5fabb65bb01dc032a974821ee6b4b91c74ba160ab301397718ebe2d3367583a962409dff8ae5f04c283fa48d269a59ca2a250110e6efdc6c8a9da";

const string cmp_sha_b = "c555bd80936fa07d8ce7484fcb30f1664c32502d5d3f14625c1cbf46bf5e0cd11e327db958dbb05e4d9493a28cf0303e915129e33b82f880197f48d42c19d805";

const string cmp_sha_c = "b8abd1927a5f7ea043bfcd676e360a51e579bd40ec979986457a3886da18910c0ce33878195bcc39ad2df38ba47521d0cadb37d3f1c17508ee4c1b4dfbb94f6b";

const string cmp_sha_d = "1f8ab8f2a8425355502b0eb2bac00522546cdcc888ec067072de70f322d18bfeaad275dacfd1dd2322bd6500bcfe55920c672492f26fda2f2cfeabcbfef881ae";

int main(int argc, char** argv) {
    size_t a, b, c, d;
    cout << "Enter a, b, c, and d, all on the same line, seperated by spaces: ";
    cin >> a >> b >> c >> d;
    const bool sha_a_res = (sha512::calculate(to_string(a)) == cmp_sha_a);
    const bool sha_b_res = (sha512::calculate(to_string(b)) == cmp_sha_b);
    const bool sha_c_res = (sha512::calculate(to_string(c)) == cmp_sha_c);
    const bool sha_d_res = (sha512::calculate(to_string(d)) == cmp_sha_d);
    if (sha_a_res & sha_b_res & sha_c_res & sha_d_res) {
        if (function_1(a) & function_2(b) & function_3(c) & function_3(d) & a >= 1000000000000 & b >= 2000000000 & c >= 100000000000000 & d >= 10000000000000000) {
            cout << "Stage 2: https://rentry.co/" << to_string((((a^b^c^d)<<32)%0x100000001b3ULL)<<2) << "\n";
        } else {
            cout << "SHA checks passed but function tests did not! If this happens please open a ticket." << endl;
        }
    } else {
        cout << "Incorrect values entered for a, b, c, and/or d\n";
    }
    return 0;
}