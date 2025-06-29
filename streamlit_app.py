
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import math
from scipy.special import expit
 

st.set_page_config(page_title="Credit Risk Game", page_icon="💰")

st.markdown("""
    <style>
    
    .main {
        background: linear-gradient(135deg, #74ebd5 0%, #ACB6E5 100%);
        min-height: 100vh;
        padding: 2rem 1rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .title {
        text-align: center;
        color: #0B3D91;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.25);
        font-size: 3rem;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #146C94;
        font-size: 1.5rem;
        margin-top: 0.2rem;
        margin-bottom: 2rem;
    }
    
    div.stButton > button {
        background-color: #0B3D91;
        color: white;
        border-radius: 12px;
        padding: 12px 24px;
        font-size: 1.1rem;
        font-weight: 600;
        transition: background-color 0.3s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #146C94;
        cursor: pointer;
    }
    
    .stColumns {
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .header-img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 120px;
        margin-bottom: 1rem;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.25));
    }
    </style>
""", unsafe_allow_html=True)


if "level" not in st.session_state:
    st.session_state.level = 0 


if st.session_state.level == 0:
  
    st.markdown("""
        <img class="header-img" src="https://cdn-icons-png.flaticon.com/512/633/633611.png" alt="Credit Risk Icon" />
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="title">🎓 Credit Risk Game</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="subtitle">Choose a level to begin:</h3>', unsafe_allow_html=True)

    cols = st.columns(3)
    for i in range(1, 7): 
        with cols[(i - 1) % 3]:
            if st.button(f"Level {i}"):
                st.session_state.level = i
# === LEVEL 1 ===
elif st.session_state.level == 1:
    st.header("📘 Level 1: Income & Credit History")
    st.markdown("So, what is this credit risk? To explane it with simple wrods, credit risk is *the possibility of a loss resulting from a borrower´s failure to repay a loan or meet contractual obligations*. ")
    st.markdown("Therefore, is it so important for banks to have a way of calculation these credit risk. Then we are going to talk, how exactly do they do it. The amount, term and interest rate of the loan depend on this parameter (more details in the following levels)")
    st.markdown("To manage this risk, three key parameter are used:***Probability of Default* (PD)**, ***Loss Given Default* (LGD)  , and  *Exprosure at Default* (EAD)**. And **EL(*Expected Losses*)** can be calculated as **EL=PD×LGD×EAD** (these formula use many banks), which shows the average potential loss considering the risk. To anticipate risks, data about the client is also needed-such as income, age, cresit history etc. We will explore it in detail in the next levels, but you can try a simulator(primitive, uses only 3 parametrs, such as income and simple credit history(just 4 options)) but later we can apply more advanced methods. ")
    st.subheader("💰Simulator")
    name = st.text_input("            Write the name of the client")
    income = st.slider(
        label="    His/her income ($ per month)",
        min_value=500,
        max_value=10000,
        value=2500,
        step=50
    )
    loan_amount = st.slider("Requested loan amount ($)", 500, 10000, 2000)
    history = st.selectbox(
    "      Credit history ",
    ["Excellent", "Good", "Average", "Poor"],
    index=1 
    )
    st.subheader("Understanding Credit History 📊")

    with st.expander("#### 🟢 Excellent"):
        st.markdown("""
        - ✅ Always pays on time  
        - ✅ No late payments  
        - ✅ Very low or no outstanding debt  
        - ✅ Long history of responsible credit use  

    **📊 Very low credit risk**  
    _Likely to receive the best loan terms and highest approval chances._
    """)

    with st.expander("#### 🟡 Good"):
        st.markdown("""
        - ⚠️ Occasional late payments (1–2 in recent years)  
        - ✅ Generally responsible borrower  
        - ✅ Moderate debt level, no major issues  

    **📊 Low to moderate credit risk**  
    _Likely to be approved, but with slightly less favorable terms._
    """)

    with st.expander("#### 🟠 Average"):
        st.markdown("""
        - ⚠️ Several late payments (3–5)  
        - 🔄 History of minor loan problems or missed payments  
        - 💳 High credit utilization or debt levels  

    **📊 Moderate to high credit risk**  
    _May still qualify, but with stricter conditions or lower limits._
    """)

    with st.expander("#### 🔴 Poor"):
        st.markdown("""
        - ❌ Frequent late payments  
        - ❌ Defaults, collections, or serious credit issues  
        - ❌ Often exceeds credit limits  

    **📊 High credit risk**  
    _Most lenders will deny the loan or offer very limited options._
    """)

    if history == "Excellent":
        multiplier = 1.0
    elif history == "Good":
        multiplier = 1.5
    elif history == "Average":
        multiplier = 2.0
    else: 
        multiplier = 3.0
    base_risk = (loan_amount / (income*8) )
    risk = base_risk * multiplier
    st.markdown(f"#### Credit risk of {name} is {risk:.5f}")

    data = {
        "Risk Value": [
            "0 – 0.1",
            "0.1 – 0.3",
            "0.3 – 0.6",
            "0.6 – 1.0",
            "> 1"
        ],
        "Meaning": [
            "Very low risk, practically safe",
            "Low risk, borrower likely to repay",
            "Medium risk, possible delays",
            "High risk, repayment problems likely",
            "Very high risk or model error"
        ]
    }

    df = pd.DataFrame(data)

    st.markdown("### Credit Risk Interpretation Table")
    st.table(df)
    st.markdown("###### So, this simulator is very simple and does not take into account most of the factors, it is made simply to start understanding the logic of credit risk. Next we will learn how to use it and how to make more accurate calculations with a large amount of data🙂")
    st.markdown(" *We assume tha twe are talking about some kind of short-term simple household loan and I assigned these levels a multiplier factor for calculating credit risk as 1, 1.5, 2 and 3 respectively from the best to the worth* ")
    
    if st.button("🔙 Back to Main Menu"):
        st.session_state.level = 0
    if st.button("➡️Next Level"):
        st.session_state.level = 2
    

# === LEVEL 2 ===
elif st.session_state.level == 2:
    st.header("📗 Level 2: Client Debt")
    st.markdown("You've already seen that credit risk also *depens on ratio between the income and the loan payments*. So, Debt-to-Income Ratio (DTI) can be described as ")
    st.latex(r"DTI = \frac{\text{Monthly Debt Payments}}{\text{Gross Monthly Income}} \times 100\%")
    st.markdown("and it is certainly very important parameter, because it directly describes an ability to pay this debt as promised, due to fact that everyone needs to spend a big part of his income to food, accomodation, etc and also can appear unforeseen expenses. Therefore, we can say:DTI<20%-🟢 Low risk – likely to be approved; 20–35% - 🟡 Moderate risk – might be approved with conditions; > 35% - 🔴 High risk – likely to be rejected.")

    st.markdown("### Try to guess, who has lower risk?")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Client A**")
        st.markdown("- Income: €3000/month\n- Debt: €900/month")

    with col2:
        st.markdown("**Client B**")
        st.markdown("- Income: €2000/month\n- Debt: €500/month")

    choice = st.radio("Who is less risky?", ["Client A", "Client B"], index=None)

    show_answer = st.button("Show answer")

    if show_answer and choice:
        if choice == "Client A":
            st.error("❌ Incorrect – DTI = 30%")
        else:
            st.success("✅ Correct! Client B has DTI = 25%")

    st.markdown("## Credit Utilization Ratio (CUR)")

    st.markdown("**Credit Utilization Ratio** measures how much of your available credit you’re using. A high ratio means higher risk for lenders. It also shows the behavior of the client, therefore it is very important for banks.")

    credit_limit = st.slider("Total Credit Limit ($)", 500, 10000, 3000, step=100)
    credit_balance = st.slider("Current Credit Card Balance ($)", 0, credit_limit, 900, step=100)

    cur = round((credit_balance / credit_limit) * 100, 1)

    st.markdown("#### 🧮 Calculation:")
    st.latex(r"CUR = \frac{Credit\ Card\ Balance}{Credit\ Limit} \times 100\%")
    st.markdown(f"CUR = ({credit_balance} / {credit_limit}) × 100 = **{cur}%**")

    st.markdown("####  Credit Risk Evaluation:")
    if cur <= 10:
        st.success("🟢 **Excellent** – Very low risk. Great credit management!")
    elif cur <= 30:
        st.info("🟡 **Good** – Acceptable, but try to lower it further.")
    elif cur <= 50:
        st.warning("🟠 **Caution** – This may negatively affect credit score.")
    else:
        st.error("🔴 **High Risk** – Most lenders see this as a serious warning sign.")
        
    st.subheader("Purpose")
    st.markdown(" The purpose of lending is one of the key factors influencing the level of credit risk. Loans issued for production needs or investment projects are usually accompanied by more thorough assessment and monitoring, which reduces the likelihood of default. At the same time, consumer loans, especially unsecured ones, are often associated with increased risk, since their purpose is to meet the current personal needs of the borrower, which may be less controllable and predictable. Thus, when analyzing applications, credit institutions pay special attention to the purpose of the loan, distinguishing different categories of loans according to risk level and forming lending conditions accordingly.")

    data = {
        "Loan Purpose": [
            "Business", "Car financing", "Credit card refinancing", "Debt consolidation",
            "Home buying", "Home improvement", "Major purchase", "Medical expenses",
            "Moving and relocation", "Vacation"
        ],
        "Default (%)": [42.1, 18.1, 20.7, 24.5, 24.0, 21.0, 26.7, 27.6, 28.5, 21.6],
        "Fully Paid (%)": [57.9, 81.9, 79.3, 75.5, 76.0, 79.0, 73.3, 72.4, 71.5, 78.4]
    }

    df = pd.DataFrame(data)

    st.subheader("Table")
    st.dataframe(df)

    st.markdown("*It shows a possible correlation between purpose of the credit and statistics of default*")
    
    if st.button("🔙 Back to Main Menu"):
        st.session_state.level = 0
    if st.button("➡️Next Level"):
        st.session_state.level = 3
# === LEVEL 3 ===
elif st.session_state.level == 3:
    st.header("📙 Level 3: PD Calculations-Finals")
    st.write("So, it is time to end eith calculation of the probability of default, we will take a look at the last indicators and use math to get it!🙂")
    st.markdown("""
    #### 1️⃣ Number of Past Delinquencies  
    If a person has missed payments in the past, it’s a red flag for lenders.  
    The more late payments they have, the higher the risk that they might default again.  
    Even a single missed payment can significantly affect their creditworthiness.

    #### 2️⃣ Age  
    Younger borrowers (under 30) tend to have less financial experience and less stable income.  
    They may take more risks or mismanage debt. Older individuals usually have more stable finances and are considered lower-risk.

    #### 3️⃣ Education Level  
    Higher education often correlates with better financial knowledge and responsibility.  
    Educated borrowers are more likely to understand loan terms and make sound financial decisions, reducing their risk of default.

    #### 4️⃣ Place of Residence  
    People living in more affluent or economically stable areas typically have better access to employment and higher income levels.  
    This environment reduces their overall financial risk compared to individuals in more disadvantaged regions.

    #### 5️⃣ Employment Stability  
    Borrowers with long-term, stable jobs are less likely to experience income shocks.  
    A steady job history gives lenders confidence that the person can maintain regular loan payments.
    """)

    def plot_age_vs_pd():
        age_groups = ["18–24", "25–34", "35–44", "45–54", "55–64", "65+"]
        pd_values = [6.5, 5.0, 3.0, 2.0, 2.5, 4.0]
        fig, ax = plt.subplots()
        bars = ax.bar(age_groups, pd_values, color='lightcoral')
        ax.set_title("Probability of Default by Age Group")
        ax.set_xlabel("Age")
        ax.set_ylabel("PD (%)")
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, f"{bar.get_height()}%", ha='center')
        return fig

    def plot_location_vs_pd():
        locations = ["Urban", "Suburban", "Rural"]
        pd_values = [2.0, 3.0, 5.0]
        fig, ax = plt.subplots()
        bars = ax.bar(locations, pd_values, color='mediumseagreen')
        ax.set_title("Probability of Default by Location")
        ax.set_xlabel("Location")
        ax.set_ylabel("PD (%)")
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, f"{bar.get_height()}%", ha='center')
        return fig

    def plot_employment_stability_vs_pd():
        categories = ["< 1 yr", "1–3 yrs", "3–5 yrs", "5+ yrs"]
        pd_values = [6.0, 4.0, 2.5, 1.5]
        fig, ax = plt.subplots()
        bars = ax.bar(categories, pd_values, color='cornflowerblue')
        ax.set_title("PD by Employment Stability")
        ax.set_xlabel("Employment Duration")
        ax.set_ylabel("PD (%)")
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, f"{bar.get_height()}%", ha='center')
        return fig
    def plot_late_payments_vs_pd():
        payments = ["0", "1–2", "3–5", "6+"]
        pd_values = [1.0, 3.5, 6.0, 9.5]
        fig, ax = plt.subplots()
        bars = ax.bar(payments, pd_values, color='goldenrod')
        ax.set_title("PD by Number of Late Payments")
        ax.set_xlabel("Late Payments (past year)")
        ax.set_ylabel("PD (%)")
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, f"{bar.get_height()}%", ha='center')
        return fig

    st.title("📊 Factors Influencing Probability of Default (PD)")

    st.subheader("1. Age")
    st.pyplot(plot_age_vs_pd())

    st.subheader("2. Location")
    st.pyplot(plot_location_vs_pd())

    st.subheader("3. Employment Stability")
    st.pyplot(plot_employment_stability_vs_pd())

    st.subheader("4. Number of Late Payments")
    st.pyplot(plot_late_payments_vs_pd())
    
    st.subheader("⚔️The final fight with PD")
    st.markdown("##### Let`s take a look at math calculation with all of these parameters")
         
    
    st.latex(r"""
    \text{PD}(x) = \frac{1}{1 + e^{-(\beta_0 + \beta_1 x_1 + \beta_2 x_2 + \dots + \beta_n x_n)}}
    """)

    st.markdown("""
    Where:
    - \\( x_1, x_2, x_n ) — features (e.g., age, income, credit history)
    - \\( beta_0, beta_1, beta_n ) — coefficients from the model  
    - **PD(x)** — estimated probability of default
    """)
    st.markdown("### Z-score Formula for Credit Risk")

    st.markdown("This formula estimates the credit risk score (Z) based on key client attributes:")

    st.latex(r"""
    z = \beta_0 + \beta_1 \cdot \text{Income} + \beta_2 \cdot \text{DTI} + \beta_3 \cdot \text{Employment} + \beta_4 \cdot \text{CreditHistory} + \beta_5 \cdot \text{difference from optimal age(45)}
    """)

    st.markdown("""
    Where:

    - **Income** = client's monthly income (in thousands of €)  
    - **DTI** = debt-to-income ratio (%)  
    - **Employment** = years of stable employment  
    - **CreditHistory** = score from 0 (poor) to 1 (excellent)  
    - \( beta_0 , beta_1, beta_4 ) are the model coefficients
    """)
    st.markdown("##### *Let`s calculate ith tese 4 parametrs(but off course we can add more, such as area, education, etc.)* ")

    st.subheader("Try it via z-score")
    

    st.markdown("### Enter client information:")

    x1 = (st.slider("💰 Monthly Income ($ thousands)", 0, 10000, 3000))/1000  # уже делим на 1000 в слайдере
    x2 = st.slider("📉 DTI (%)", 0, 100, 30)
    x3 = st.slider("🧑‍💼 Stable Employment (years)", 0, 30, 5)
    x4 = st.slider("📋 Credit History Score (0=Poor, 1=Excellent)", 0.0, 1.0, 0.8)
    x5 = st.slider("👱 Age", 18, 80, 40)
    
    z = (
    -3
    - 0.0005 * x1
    + 0.1 * x2
    - 0.05 * x3
    - 1.0 * x4
    + 0.04 * abs(x5 - 45)
    )

    pd = expit(z / 3)

    st.latex(rf"z = -3 - 0.0005 \cdot {x1} + 0.1 \cdot {x2} - 0.05 \cdot {x3} - 1.0 \cdot {x4:.2f} + 0.04 \cdot |{x5} - 45| = {z:.2f}")
    st.latex(rf"PD = \frac{{1}}{{1 + e^{{-z/3}}}} = {pd:.1%}")

    if pd < 0.1:
        st.success("✅ Very Low Risk — Excellent creditworthiness")
    elif pd < 0.3:
        st.info("🟢 Low Risk — Good credit profile")
    elif pd < 0.6:
        st.warning("🟡 Moderate Risk — Review recommended")
    else:
        st.error("🔴 High Risk — Likely to default")

    st.markdown("##### Well, off course our formula is not completely proffesional, but no you better understand one of the key parameters (PD). And as you can see the bigger z, the worse.*(we assumed betas like in the formula)*")

    st.subheader("Try it yourself")

    case = {
        "A": {"Income": 7000, "DTI": 25, "Emp": 10, "Score": 0.9, "Age": 42, "z": -1.2},
        "B": {"Income": 2000, "DTI": 65, "Emp": 1,  "Score": 0.3, "Age": 22, "z": 1.8},
    }

    st.write(f"A: Income=${case['A']['Income']}, DTI={case['A']['DTI']}%, Employment={case['A']['Emp']}y, Score={case['A']['Score']}, Age={case['A']['Age']}")
    st.write(f"B: Income=${case['B']['Income']}, DTI={case['B']['DTI']}%, Employment={case['B']['Emp']}y, Score={case['B']['Score']}, Age={case['B']['Age']}")
    
    choice = st.selectbox("Who has lower credit risk (lower z)?", [" ", "A", "B"])

    if choice == "":
        st.info("Please select an option")
    else:
        correct = "A" if case["A"]["z"] < case["B"]["z"] else "B"
    if choice == correct:
        st.success("✅ Correct!")
    else:
        st.error("❌ Incorrect.")

    with st.expander("Show z-values and explanation"):
        st.write(f"z for A = {case['A']['z']}")
        st.write(f"z for B = {case['B']['z']}")
        st.write("Lower z means lower credit risk, so the borrower with the smaller z is better.")


    
    
    if st.button("🔙 Back to Main Menu"):
        st.session_state.level = 0
    if st.button("➡️Next Level"):
        st.session_state.level = 4
    



# === LEVEL 4 ===
elif st.session_state.level == 4:
    st.header("📕 Level 4: Loss Given Default (LGD) calculation")
    st.markdown("""
    In this section, you will learn what affects **LGD (Loss Given Default)** – the percentage of a loan a bank loses if the borrower defaults.

    These are the key factors that influence LGD:
    """)

    st.header("1. Collateral Type and Quality")
    st.markdown("""
    ##### To refresh the memory:
    
    Collateral helps reduce losses by backing the loan with an asset.

    - **Real estate** generally has high recovery value → lower LGD  
    - **Vehicles** or **consumer goods** lose value quickly → higher LGD  
    - **Unsecured loans** (no collateral) → very high LGD

    Better collateral leads to higher recovery and therefore lower LGD.
    """)

    st.header("2. Loan-to-Value Ratio (LTV)")
    st.markdown(r"""
    **LTV** is the ratio of the loan amount to the value of the collateral:

    LTV= Loan Amount * Collateral Value * times 100\%

    - A high LTV (e.g. 90%) means the loan is close to or exceeds the asset's value → higher LGD  
    - A lower LTV means the asset covers more of the loan → lower LGD
    """)

    st.header("3. Legal and Recovery Costs")
    st.markdown("""
    Recovering money after default often involves legal processes and administrative costs.

    - These include court fees, legal representation, repossession, and resale costs  
    - Typical costs range from 5% to 25% of the total loan or collateral value

    Higher recovery costs reduce the amount the lender can recover, increasing LGD.
    """)

    st.header("4. Recovery Time Delay")
    st.markdown("""
    The longer it takes to recover funds, the more value is lost over time due to:

    - Depreciation of assets  
    - Loss of interest income  
    - Inflation and opportunity cost

    A long delay in recovery leads to lower effective value and higher LGD.
    """)

    st.subheader("Summary Formula (Simplified)")
    st.latex(r"""
    LGD = 1 - Recovery Value
    
    """)

    st.markdown("Formula for Real Estate:")

    st.markdown(r"""
    **Formula:**

    $$
    \text{Recovery} = Q \cdot \left(1 - \frac{\text{LTV}}{150} \right) - \text{Legal\_Cost} \cdot \frac{1}{100}
    $$

    **Where:**

    - **Recovery** – the expected value recovered by the lender after default  
    - **Q** – the quality factor of the collateral (e.g., condition or liquidity of the asset)  
    - **LTV (Loan-to-Value)** – the ratio of the loan amount to the appraised value of the asset  
    - **Legal_Cost** – costs associated with legal enforcement or recovery procedures  

    """)

    
    

    st.subheader("Case:")

    collateral = "Real Estate"
    ltv = 80
    legal_cost = 10  # %
    delay_years = 2

    st.write(f"""
    - 🔒 Collateral: **{collateral}**
    - 📊 Loan-to-Value (LTV): **{ltv}%**
    - ⚖️ Legal Costs: **{legal_cost}%**
    - ⏳ Recovery Delay: **{delay_years} years**
    """)


    guess = st.selectbox("What is the LGD?", ["", "25%", "40%", "90%", "75%"])


    collateral_quality = 0.8  
    base_recovery = collateral_quality * (1 - ltv / 150)
    base_recovery -= legal_cost / 100
    base_recovery *= (1 - 0.05 * delay_years)
    base_recovery = max(0, min(base_recovery, 1))
    lgd = 1 - base_recovery
    true_lgd_percent = round(lgd * 100)

    if guess:
        user_lgd = int(guess.strip('%'))
        if user_lgd == true_lgd_percent:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect. Correct answer: **{true_lgd_percent}%**")

        with st.expander("🧠 Explanation"):
            st.latex(r"\text{Recovery} = Q \cdot (1 - \frac{LTV}{150}) - \text{Legal Cost} \cdot \frac{1}{100}")
            st.write(f"→ Collateral Quality = {collateral_quality}")
            st.write(f"→ Recovery = {base_recovery:.2f}")
            st.write(f"→ LGD = 1 - Recovery = **{true_lgd_percent}%**")


    if st.button("➡️Next Level"):
            st.session_state.level = 5
    if st.button("🔙 Back to Main Menu"):
            st.session_state.level = 0


# === LEVEL 5 ===
elif st.session_state.level == 5:
    st.header("📒 Level 5: Exprosure at Default (EAD)")
        
    st.markdown("""
    

    ### What does EAD include?

    - The **current outstanding balance** on the loan — money already drawn by the borrower.  
    - **Undrawn credit limits or credit lines** — potential amounts the borrower may draw before defaulting.  
    - For some loans, like mortgages, EAD typically equals the outstanding balance, as no additional amounts are usually drawn.

    ---

    ### Why is accurate EAD estimation important?

    1. **Risk assessment accuracy:**  
       Underestimating EAD leads to underestimating potential losses and insufficient capital reserves.

    2. **Regulatory compliance:**  
       Basel II and III require precise EAD calculation for capital adequacy.

    3. **Different approaches for different loan types:**  
       - For **revolving credits** (credit cards, lines of credit), estimating likely usage of undrawn limits is critical.  
       - For **term loans** (mortgages, auto loans), EAD often equals the current balance.

    ---

    ### How is EAD estimated?

    - **Historical borrower behavior:**  
      Analyzing past usage patterns before defaults.

    - **Statistical models:**  
      Logistic regression and other techniques to predict likely future drawings.

    - **Expert judgement and macroeconomic factors:**  
      Adjustments based on broader economic outlooks.

    ---

    ### Practical examples

    $$
    EAD = Used + Utilisation Rate * Limit-Used
    $$
    
    - **Credit card:**  
      Limit: \$10,000  
      Used: \$7,000  
      Estimated usage of undrawn limit before default(Utilisation Rate): 80% of \$3,000  

    $$
    EAD = 7,000 + 0.8 \\times 3,000 = 9,400
    $$

    - **Mortgage loan:**  
      Outstanding balance: \$150,000  
      No additional drawings expected.  

    $$
    EAD = 150,000
    $$

    ---

    ### Important notes

    - **Collateral impact:**  
        EAD measures gross exposure; collateral affects LGD instead.

    - **Netting agreements:**  
        Offsetting exposures may reduce effective EAD.

    ---

    ### Quotes from experts

    > *"EAD captures the amount the lender is exposed to at the time of default, which includes both drawn and undrawn amounts that may be drawn before default."* — Basel Committee on Banking Supervision

    > *"Accurate EAD estimation is critical to risk management and regulatory capital calculations."* — Moody’s Analytics

    > *"Undrawn commitments are a significant source of risk, especially in revolving credit facilities."* — Journal of Credit Risk
    """)
    
    st.subheader("Minigame")

    st.subheader("Case:")

    collateral = "Shown a credit scenario with parameters such as:"
    limit = 10000
    Used = 6000  
    Utilisation_Rate = 70

    st.write(f"""
    - 🔒  **{collateral}**
    - limit($): **{limit}**
    - Used($): **{Used}**
    - Utilisation Rate(%): **{Utilisation_Rate}**
    """)


    guess = st.selectbox("What is the EAD?", ["", "5300", "9700", "8800", "7400"])

    

    if guess:
        user_ead = int(guess.strip(''))
        if user_ead == 8800:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect. Correct answer: **8800**")

        with st.expander("🧠 Explanation"):
            st.markdown("EAD=Used Amount+(Undrawn Amount*Utilization Rate)")
            st.markdown("EAD=6,000+(4,000×0.7)=6,000+2,800=8,800")
    
    if st.button("➡️Next Level"):
            st.session_state.level = 6
    
    if st.button("🔙 Back to Main Menu"):
        st.session_state.level = 0

# === LEVEL 6 ===
elif st.session_state.level == 6:
    st.header("📓 Level 6: What does this give us?")
    st.write("###### Congratulations! Now you can calculate all components of expected losses, but what does it give us?🤔")

    st.markdown("""
    ## 📘 Theory: How PD, LGD, and EAD Shape Loan Terms

    Banks don't only assess **credit risk** to decide whether to approve a loan — they also use it to set **loan conditions**: interest rate, loan amount, duration, and collateral.

    1 more time:

    - **PD (Probability of Default):** Likelihood that a borrower will default.
    - **LGD (Loss Given Default):** Expected loss if default happens, after recoveries.
    - **EAD (Exposure at Default):** Total value the bank is exposed to at the moment of default.

    ---

    > “Risk-based pricing models incorporate the expected loss (EL = PD × LGD × EAD) to align interest rates with the borrower's risk profile.”  
    > — *Basel Committee on Banking Supervision (BCBS), 2017*
    
    > “Banks seek to maximize risk-adjusted return on capital (RAROC), which depends on how efficiently they manage credit risk exposures through pricing and structure.”  
    > — *Moody’s Analytics, Credit Risk Modelling Frameworks, 2021*

    ---

    ## 🧮 Example Mapping of Risk to Terms

    | Situation                      | Risk Metric Involved   | Impact on Loan Terms                                   |
    |-------------------------------|------------------------|--------------------------------------------------------|
    | Borrower with high PD         | PD                     | ↑ Interest Rate, ↓ Loan Amount, ↑ Monitoring           |
    | Collateral is low-quality     | LGD                    | ↑ Collateral Required, ↓ Approved Loan-to-Value (LTV)  |
    | High exposure amount          | EAD                    | ↓ Loan Limit, Shorter Term, Stricter Conditions        |
    | High Expected Loss (EL)       | PD×LGD×EAD             | Rejection or Significantly Higher Interest             |

    ---

    ## 🔬 Real-World Application

    Banks simulate different scenarios using **credit scoring models**, and then match borrowers into **risk buckets** (e.g. low, medium, high risk). These buckets are tied to pricing policies:

    - **Low-risk:** Competitive interest rates, flexible terms.
    - **Medium-risk:** Moderate rates, more documentation, lower limits.
    - **High-risk:** High rates or rejection, unless risk is mitigated with collateral.


    ## 🧠 Beyond EL: Capital and Margin

    Banks also apply:

    - **Capital requirements** → More risky loans require more capital.
    - **Profit margins** → Interest rate must exceed EL + cost of capital.

    Thus, even if a loan is approved, a high EL can mean **less favorable terms** to compensate for the risk.

    ---
    """)
    st.markdown("""
### How Banks React to Credit Risk

Banks and lenders actively adjust loan conditions based on perceived risk. According to a **BIS Working Paper**,  
> *"A higher risk estimate is associated with higher interest rates,"*  
though the relationship is *"weaker in competitive environments."*  
Even when multiple banks compete for clients, they still penalize risky borrowers with higher pricing.

The **European Central Bank** emphasizes that in times of market stress, the cost of capital rises sharply for weaker firms:  
> *"The expected probability of default rises by 0.2 percentage points, while corporate bond spreads increase by around 70 basis points three weeks after a risk-off shock."*

In terms of environmental risk, a 2023 study cited by the **Financial Times** found:  
> *"Eurozone banks are already factoring in climate-related risks by charging higher interest rates to companies with higher carbon emissions."*  
This so-called *climate premium* leads brown-sector borrowers to pay **up to 0.14 percentage points more** than greener counterparts — especially during periods of monetary tightening.

On the flip side, companies with strong ESG profiles enjoy better terms. According to **Federated Hermes**:  
> *"Companies with better ESG practices tend to have lower CDS spreads, even after controlling for credit risks."*

""")

    
    if st.button("🔙 Back to Main Menu"):
        st.session_state.level = 0

