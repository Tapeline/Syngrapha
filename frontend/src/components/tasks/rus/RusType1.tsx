import TaskBase from "../TaskBase.tsx";
import {useState} from "react";
import {Input} from "../../ui/input.tsx";

export type RusType1Data = {
    id: number | string;
    task: string;
    before: string,
    after: string,
    solved: boolean
}

export default function RusType1(
    {
        data,
        onBackClick = () => window.history.back(),
    }: {
        data: RusType1Data;
        onBackClick?: () => void;
    }
) {
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [answer, setAnswer] = useState<string | null>(null);
    return <TaskBase
        subject="Русский язык"
        typeNo="1"
        taskId={data.id.toString()}
        isSolved={data.solved}
        isSubmitting={isSubmitting}
        setIsSubmitting={setIsSubmitting}
        canSubmit={!!answer}
        getAnswer={() => answer || ""}
        onBackClick={onBackClick}
    >
        <p>
           <b>{data.task}</b>
        </p>
        <p>
            {data.before}
            <Input
                type="text"
                placeholder="Ответ"
                className="mx-2 w-auto inline h-[1.7em]"
                disabled={isSubmitting}
                onChange={e => setAnswer(e.target.value)}
            />
            {data.after}
        </p>
    </TaskBase>
}
