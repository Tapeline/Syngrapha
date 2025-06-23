import {useState} from "react";
import {Popover, PopoverContent, PopoverTrigger} from "../ui/popover.tsx";
import {Button} from "../ui/button.tsx";
import {CheckIcon, ChevronsUpDownIcon} from "lucide-react";
import {Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList} from "../ui/command.tsx";
import {cn} from "../../lib/utils.ts";

export default function Combobox(
    {
        values,
        initial,
        hint,
        notFound,
        onChange
    }: {
        initial: string,
        values: Array<{value: string, label: string}>,
        hint: string,
        notFound: string
        onChange: (newValue: string) => void;
    }
) {
    const [open, setOpen] = useState(false)
    const [value, setValue] = useState(initial)

    return (
        <Popover open={open} onOpenChange={setOpen}>
            <PopoverTrigger asChild>
                <Button
                    variant="outline"
                    role="combobox"
                    aria-expanded={open}
                    className="w-full justify-between"
                >
                    {value
                        ? values.find(
                            (v) => v.value === value
                        )?.label
                        : hint}
                    <ChevronsUpDownIcon className="ml-2 h-4 w-4 shrink-0 opacity-50"/>
                </Button>
            </PopoverTrigger>
            <PopoverContent className="w-full p-0">
                <Command>
                    <CommandInput placeholder={hint}/>
                    <CommandList>
                        <CommandEmpty>{notFound}</CommandEmpty>
                        <CommandGroup>
                            {values.map((v) => (
                                <CommandItem
                                    key={v.value}
                                    value={v.value}
                                    onSelect={(currentValue) => {
                                        setValue(currentValue)
                                        setOpen(false)
                                        onChange(currentValue)
                                    }}
                                >
                                    <CheckIcon
                                        className={cn(
                                            "mr-2 h-4 w-4",
                                            value === v.value ? "opacity-100" : "opacity-0"
                                        )}
                                    />
                                    {v.label}
                                </CommandItem>
                            ))}
                        </CommandGroup>
                    </CommandList>
                </Command>
            </PopoverContent>
        </Popover>
    )
}
