import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle
} from "../ui/card.tsx";
import {Button} from "../ui/button.tsx";
import {CheckIcon} from "lucide-react";
import LoaderIf from "../LoaderIf.tsx";
import {useAuthStore} from "../../hooks/auth.ts";
import {useToaster} from "../../hooks/toast.ts";
import {submitAnswer} from "../../api/tasks.ts";
import {useState} from "react";

export default function TaskBase(
    {
        subject,
        typeNo,
        taskId,
        isSolved,
        isSubmitting,
        setIsSubmitting,
        canSubmit,
        onBackClick = () => window.history.back(),
        getAnswer,
        children,
    } : {
        subject: string | React.ReactNode;
        typeNo: string;
        taskId: string;
        isSolved: boolean;
        isSubmitting: boolean;
        setIsSubmitting: (isSubmitting: boolean) => void;
        getAnswer: () => string;
        canSubmit: boolean;
        onBackClick?: () => void;
        children: any;
    }
) {
    const {accessToken} = useAuthStore();
    const {toast} = useToaster();
    const [isTaskSolved, setIsTaskSolved] = useState(isSolved);
    const handleSubmit = () => {
        setIsSubmitting(true);
        submitAnswer(accessToken, taskId, getAnswer()).then(resp => {
            if (!resp.success) toast("Не удалось отправить ответ");
            if (resp.data.correct) {
                toast("Верно");
                setIsTaskSolved(true);
            } else toast("Неверно")
            setIsSubmitting(false);
        })
    }
    return <Card>
        <CardHeader>
            <CardTitle>
                {isTaskSolved && <CheckIcon className="m-1"/>}
                Тип {typeNo} (#{taskId})
            </CardTitle>
            <CardDescription>{subject}</CardDescription>
        </CardHeader>
        <CardContent>
            {children}
        </CardContent>
        <CardFooter>
            <Button variant="outline" onClick={onBackClick} className="mr-2">Назад</Button>
            <Button onClick={handleSubmit} disabled={isSubmitting || !canSubmit}>
                Ответить
                <LoaderIf src={isSubmitting}/>
            </Button>
        </CardFooter>
    </Card>
}