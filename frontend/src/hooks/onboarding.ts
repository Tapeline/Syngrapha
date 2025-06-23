import type {OnboardingTour, StoredTourState} from "../onboarding/schemas.ts";

const OB_STORE_KEY = "myapp-onboarding";

function setDefaultState(onboardingSchemas: OnboardingTour[]) {
    const data = {};
    for (const tour of onboardingSchemas)
        data[tour.id] = {completed: false, step: null};
    saveData(data);
    return data;
}

function loadData(onboardingSchemas: OnboardingTour[]) {
    if (!localStorage.getItem(OB_STORE_KEY)) setDefaultState(onboardingSchemas);
    let data;
    try {
        data = JSON.parse(localStorage.getItem(OB_STORE_KEY) || "");
    } catch (e) {
        console.error(e);
        data = setDefaultState(onboardingSchemas);
    }
    return data;
}

function saveData(data: object) {
    localStorage.setItem(OB_STORE_KEY, JSON.stringify(data));
}

export function useOnboardingStore(onboardingSchemas: OnboardingTour[]) {
    loadData(onboardingSchemas);
    return {
        setCurrentStep: (tourId: string, stepId: string) => {
            const data = loadData(onboardingSchemas);
            data[tourId].step = stepId;
            saveData(data);
        },
        setCompleted: (tourId: string, isCompleted: boolean = true) => {
            const data = loadData(onboardingSchemas);
            data[tourId].completed = isCompleted;
            saveData(data);
        },
        getTourState: (tourId: string): StoredTourState => {
            return loadData(onboardingSchemas)[tourId];
        },
        getData: () => loadData(onboardingSchemas),
    }
}
