# [api link](https://replicate.com/lucataco/florence-2-large/api)

### Set the REPLICATE_API_TOKEN environment variable

```env
REPLICATE_API_TOKEN=r8_eOQ**********************************
```

### Install Replicate’s Python client library
```bash
pip install replicate
```

Run lucataco/florence-2-large using Replicate’s API. Check out the model's schema for an overview of inputs and outputs.

```python
import replicate

input = {
    "image": "https://replicate.delivery/pbxt/L9zDhV2KiVnudUyRiNjt9P18LZ98Hrqq5GGdx9szmBCAyEhP/car.jpg",
    "task_input": "Object Detection"
}

output = replicate.run(
    "lucataco/florence-2-large:da53547e17d45b9cfb48174b2f18af8b83ca020fa76db62136bf9c6616762595",
    input=input
)

print(output)
#=> {"img":"https://replicate.delivery/pbxt/OSFBuet9KTQOF6BpG...
````